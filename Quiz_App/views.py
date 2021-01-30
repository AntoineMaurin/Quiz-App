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
    request.session['question_number'] = 0
    request.session['questions_left'] = ids_list
    request.session['quiz_id'] = quiz.id

    return render(request, "welcome_quiz.html", {'quiz': quiz})

def nextquestionpage(request):

    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    try:
        current_question_id = request.session['questions_left'][0]
        current_question = Question.objects.get(id=current_question_id)
        checked_answers = request.POST.getlist('is_answer_checked')


        if 'quiz_results' in request.session:
            request.session['quiz_results'][str(current_question.title)] = checked_answers
        else:
            request.session['quiz_results'] = {}

        request.session['question_number'] += 1
        del(request.session['questions_left'][0])
        request.session.modified = True

        return render(request, "quiz_question_playing.html", {'quiz': quiz,
                                                              'current_question': current_question,
                                                              'question_number': request.session['question_number'],
                                                              })
    except(IndexError):

        all_questions = Question.objects.filter(quiz=quiz)
        # Generates results of the quiz played
        quiz_results = request.session['quiz_results']
        # del(request.session['quiz_results'])
        # request.session.modified = True

        return render(request, "quiz_results.html", {'quiz': quiz,
                                                     'all_questions': all_questions,
                                                     'quiz_results': quiz_results})
