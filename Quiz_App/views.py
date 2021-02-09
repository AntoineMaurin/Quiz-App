from django.shortcuts import render
from Quiz_App.models import Quiz, Question, Answer
from django.contrib import messages


def discoverpage(request):
    quizzes = Quiz.objects.filter(is_public=True)
    return render(request, "discoverpage.html", {'quizzes': quizzes})

def playpage(request):
    return render(request, "play.html")

def startquizpage(request, id):
    if id == 0:
        id = request.GET['quiz_id']
    try:
        quiz = Quiz.objects.get(id=id)
    except(Quiz.DoesNotExist):
        messages.error(request, "This quiz code doesn't exist..")
        return render(request, "play.html")

    questions = Question.objects.filter(quiz=quiz)
    if len(questions) < 1:
        messages.error(request, 'Sorry, this quiz does not contain any '
                       'questions, please try another one.')
        return discoverpage(request)
    ids_list = []
    for question in questions:
        ids_list.append(question.id)
    request.session['question_number'] = 1
    request.session['questions_left'] = ids_list
    request.session['quiz_id'] = quiz.id

    return render(request, "welcome_quiz.html", {'quiz': quiz})

"""This view makes the quiz work while being played. It manages to render
the different questions of the quiz, and generate the quiz results when
finished."""
def nextquestionpage(request):

    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    try:
        # In this part we get the current question, which is referenced by its
        # id in the session dictionnary. And then we get the answers that the
        # user checked for this question.
        current_question_id = request.session['questions_left'][0]
        current_question = Question.objects.get(id=current_question_id)
        checked_answers = request.POST.getlist('is_answer_checked')

        # Builds a list that will store the answers of each question
        if 'quiz_results' in request.session:

            request.session['question_number'] += 1
            # Each time this view is called, it renders the first question of
            # the list, so here i delete the last question played to go to the
            # next one.
            del(request.session['questions_left'][0])
            request.session.modified = True

            # Here i add the question as a key and the checked answers as value
            # in the 'quiz_resulst' dictionnary that i pass in the session dict
            request.session['quiz_results'].append([current_question_id, checked_answers])

            current_question_id = request.session['questions_left'][0]
            current_question = Question.objects.get(id=current_question_id)

        else:
            request.session['quiz_results'] = []

        return render(request, "quiz_question_playing.html", {'quiz': quiz,
                                                              'current_question': current_question,
                                                              'question_number': request.session['question_number'],
                                                              })
    # If there is no question left, generates the quiz_resulst page
    except(IndexError):

        quiz_results = request.session['quiz_results']

        # Transforms every question ID into its related Question object.
        for elt in quiz_results:
            question = Question.objects.get(id=elt[0])
            elt[0] = question

        success_rate = success_rate_calcul(quiz_results, quiz)

        # The quiz is now finished, so to replay it or play another, a reset is
        # needed.
        del(request.session['quiz_results'])
        del(request.session['quiz_id'])
        request.session.modified = True

        return render(request, "quiz_results.html", {'quiz': quiz,
                                                     'success_rate': success_rate,
                                                     'quiz_results': quiz_results})

def success_rate_calcul(quiz_results, quiz):
    right_answers = 0
    wrong_answers = 0

    all_answers = Answer.objects.filter(question__quiz=quiz)

    checked_answers = []
    for question_and_answerslist in quiz_results:
        for checked_answer in question_and_answerslist[1]:
            checked_answers.append(checked_answer)

    for answer in all_answers:
        if answer.title in checked_answers and answer.is_right:
            right_answers += 1
        elif answer.title in checked_answers and not answer.is_right:
            wrong_answers += 1

    try:
        success_rate = (right_answers/(right_answers + wrong_answers)) * 100
    except(ZeroDivisionError):
        success_rate = 0
        
    return success_rate
