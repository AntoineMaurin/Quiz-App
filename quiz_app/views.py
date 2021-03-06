from django.shortcuts import render
from quiz_app.models import Quiz, Question, Answer
from django.contrib import messages


def discoverpage(request):
    quizzes = Quiz.objects.filter(is_public=True)
    return render(request, "discoverpage.html", {'quizzes': quizzes})

def playpage(request):
    return render(request, "play.html")

def startquizpage(request, quiz_id):

    if quiz_id == 0:
        quiz_id = request.GET['quiz_id']

    state, message = test_quiz_integrity(request, quiz_id)

    if state == "does not exist":
        messages.error(request, message)
        return render(request, "play.html")
    elif state == "zero questions":
        messages.error(request, message)
        return discoverpage(request)
    else:
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)

        ids_list = []
        for question in questions:
            ids_list.append(question.id)
        request.session['question_number'] = 1
        request.session['questions_left'] = ids_list
        request.session['quiz_id'] = quiz.id

        return render(request, "welcome_quiz.html", {'quiz': quiz})

"""This view manages the questions when a quiz is played. It renders the
different questions of the quiz, and generates the quiz results when
finished."""
def nextquestionpage(request):

    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    try:
        current_question_id = request.session['questions_left'][0]
        current_question = Question.objects.get(id=current_question_id)
        checked_answers = request.POST.getlist('checked_answer')
        checked_answers_ids = []

        current_question_answers = Answer.objects.filter(
            question=current_question
            )
        for answer in current_question_answers:
            if answer.title in checked_answers:
                checked_answers_ids.append(answer.id)

        if 'quiz_results' in request.session:

            if len(checked_answers) < 1:
                messages.error(request, "You haven't checked any answer :)")
                context = {'quiz': quiz,
                           'current_question': current_question,
                           'question_number': request.session['question_number']}
                return render(request, "quiz_question_playing.html", context)

            request.session['question_number'] += 1

            del(request.session['questions_left'][0])
            request.session.modified = True

            request.session['quiz_results'].append([current_question_id,
                                                    checked_answers_ids])

            current_question_id = request.session['questions_left'][0]
            current_question = Question.objects.get(id=current_question_id)

        else:
            request.session['quiz_results'] = []

        context = {'quiz': quiz,
                   'current_question': current_question,
                   'question_number': request.session['question_number']}
        return render(request, "quiz_question_playing.html", context)

    # No questions left, preparing the quiz results
    except(IndexError):

        quiz_results = request.session['quiz_results']

        for question_data in quiz_results:
            question = Question.objects.get(id=question_data[0])
            question_data[0] = question

        success_rate = calcul_success_rate(quiz_results, quiz)

        del(request.session['quiz_results'])
        del(request.session['quiz_id'])
        request.session.modified = True

        context = {'quiz': quiz,
                   'success_rate': success_rate,
                   'quiz_results': quiz_results}
        return render(request, "quiz_results.html", context)


def cancelquiz(request):
    if request.POST:
        del(request.session['quiz_results'])
        del(request.session['quiz_id'])
        request.session.modified = True
    return discoverpage(request)


def calcul_success_rate(quiz_results, quiz):
    right_answers = 0
    wrong_answers = 0

    checked_answers_ids = []
    for question_and_answerslist in quiz_results:
        for checked_answer in question_and_answerslist[1]:
            checked_answers_ids.append(checked_answer)

    for answer_id in checked_answers_ids:
        related_answer_object = Answer.objects.get(id=answer_id)
        if related_answer_object.is_right:
            right_answers += 1
        else:
            wrong_answers += 1

    try:
        success_rate = (right_answers/(right_answers + wrong_answers)) * 100
    except(ZeroDivisionError):
        success_rate = 0

    return success_rate


def test_quiz_integrity(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except(Quiz.DoesNotExist):
        return "does not exist", "This quiz code doesn't exist.. try another !"

    questions = Question.objects.filter(quiz=quiz)
    if len(questions) < 1:
        return "zero questions", ("Hmm, this quiz does not contain any "
                                 "questions.. try another one ?")
    else:
        return "all good", ""

def search(request):
    text = request.GET.get('search_text')
    difficulty = request.GET.get('difficulty')
    language = request.GET.get('language')

    if difficulty == "all" and language == "all":
        quizzes = Quiz.objects.filter(is_public=True,
                                      title__unaccent__icontains=text)
    elif difficulty == "all" and not language == "all":
        quizzes = Quiz.objects.filter(is_public=True,
                                      title__unaccent__icontains=text,
                                      language=language)
    elif not difficulty == "all" and language == "all":
        quizzes = Quiz.objects.filter(is_public=True,
                                      title__unaccent__icontains=text,
                                      difficulty=difficulty)
    else:
        quizzes = Quiz.objects.filter(is_public=True,
                                      title__unaccent__icontains=text,
                                      difficulty=difficulty,
                                      language=language)
    return render(request, "discoverpage.html", {'quizzes': quizzes})
