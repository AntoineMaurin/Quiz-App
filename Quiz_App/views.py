from django.shortcuts import render
from Quiz_App.models import Quiz, Question, Answer
from django.contrib import messages


def discoverpage(request):
    quizzes = Quiz.objects.filter(is_public=True)
    return render(request, "discoverpage.html", {'quizzes': quizzes})

def playpage(request):
    if request.method == 'POST':
        quiz_id = request.session['quiz_id']
        messages.success(request, 'Your quiz had been successfully created ! '
                                  'your quiz code is {}'.format(quiz_id))
    return render(request, "play.html")

def startquizpage(request):
    id = request.GET['quiz_id']
    quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)
    ids_list = []
    for question in questions:
        ids_list.append(question.id)
    request.session['question_number'] = 1
    request.session['questions_left'] = ids_list
    request.session['quiz_id'] = quiz.id

    return render(request, "welcome_quiz.html", {'quiz': quiz})

def nextquestionpage(request):

    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    # Tests if there is still questions left
    try:
        # Gets the first question of the list, gets the real Question object,
        # and gets the list of answers checked.
        current_question_id = request.session['questions_left'][0]
        current_question = Question.objects.get(id=current_question_id)
        checked_answers = request.POST.getlist('is_answer_checked')

        # Builds a dictionnary that will store the answers of each question
        if 'quiz_results' in request.session:

            request.session['question_number'] += 1
            # Each time this view is called, it renders the first question of
            # the list, so here i delete the last question played
            del(request.session['questions_left'][0])
            request.session.modified = True

            # Here i add the question as a key and the checked answers as value
            # in the 'quiz_resulst' dictionnary that i pass in the session dict
            request.session['quiz_results'].append([current_question_id, checked_answers])
            print(request.session['quiz_results'])
            # Updates the list of questions left for the next one
            current_question_id = request.session['questions_left'][0]
            current_question = Question.objects.get(id=current_question_id)

        # If the dictionnary doesn't exist, create it (before the 1st question)
        else:
            request.session['quiz_results'] = []

        return render(request, "quiz_question_playing.html", {'quiz': quiz,
                                                              'current_question': current_question,
                                                              'question_number': request.session['question_number'],
                                                              })
    # If there is no question left, generates the quiz_resulst page
    except(IndexError):

        quiz_results = request.session['quiz_results']

        for elt in quiz_results:
            question = Question.objects.get(id=elt[0])
            elt[0] = question

        del(request.session['quiz_results'])
        request.session.modified = True

        return render(request, "quiz_results.html", {'quiz': quiz,
                                                     'quiz_results': quiz_results})
