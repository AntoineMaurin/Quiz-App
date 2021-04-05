from django.shortcuts import render, redirect
from quiz_app.models import Quiz, Question, Answer
from django.contrib import messages
import random


def discoverpage(request):
    language = get_language(request)
    quizzes = Quiz.objects.filter(is_public=True,
                                  language=language).distinct("title")
    return render(request, "discoverpage.html", {'quizzes': quizzes})

def playpage(request):
    return render(request, "play.html")

def pick_a_difficulty(request, quiz_slug=""):

    if quiz_slug == "":
        requested_quiz = Quiz.objects.get(id=request.GET['quiz_id'])
        quiz_slug = requested_quiz.slug

    language = get_language(request)
    quizzes = Quiz.objects.filter(slug=quiz_slug,
                                  language=language)
    request.session['question_number'] = 0

    return render(request, "welcome_quiz.html", {'quizzes': quizzes})

def playquiz(request, difficulty, quiz_slug):

    if request.session['question_number'] == 0:
        setup_quiz(request, difficulty, quiz_slug)

    quiz = Quiz.objects.get(id=request.session['quiz_id'])

    checked_answer = request.POST.get('checked_answer', '')

    current_question = get_current_question(request)

    if not checked_answer:
        if 'answered_questions_ids' in request.session:
            if request.session.get('lang', 'fr') == 'fr':
                message = "Vous n'avez pas coché de réponse"
            else:
                message = "You haven't checked any answer"
            messages.error(request, message)
        else:
            request.session['answered_questions_ids'] = []

        context = {'question_number': request.session['question_number'] + 1,
                   'question': current_question,
                   'quiz': quiz}
        return render(request, "quiz_question_playing.html", context)

    append_quiz_results(request, current_question.id, checked_answer)
    request.session['question_number'] += 1

    current_question = get_current_question(request)

    if not current_question:
        # calcultate results
        success_rate = calcul_success_rate(
            request.session['answered_questions_ids']
            )
        context = {'quiz': quiz,
                   'success_rate': success_rate,
                   'answered_questions_ids': request.session['answered_questions_ids']}
        clean_session_dict(request)
        return render(request, "quiz_results.html", context)

    context = {'question_number': request.session['question_number'] + 1,
               'question': current_question,
               'quiz': quiz}

    return render(request, "quiz_question_playing.html", context)

def clean_session_dict(request):
    try:
        del(request.session['quiz_id'])
        del(request.session['questions_ids'])
        del(request.session['question_number'])
        del(request.session['answered_questions_ids'])
        request.session.modified = True
    except(KeyError):
        pass

def setup_quiz(request, difficulty, quiz_slug):
    quiz = Quiz.objects.get(slug=quiz_slug,
                            difficulty=difficulty,
                            language=get_language(request))
    request.session['quiz_id'] = quiz.id
    request.session['questions_ids'] = get_questions_ids(quiz)

def get_current_question(request):
    try:
        question_id = request.session['questions_ids'][
            request.session['question_number']
            ]
        current_question = Question.objects.get(id=question_id)
        return current_question
    except(IndexError):
        return None

def get_questions_ids(quiz):
    quiz_questions = Question.objects.filter(quiz=quiz)
    questions_ids = [question.id for question in quiz_questions]
    return questions_ids

def append_quiz_results(request, question_id, answer_title):
    for answer in Answer.objects.filter(question__id=question_id):
        if answer.title == answer_title:
            request.session['answered_questions_ids'].append(answer.id)

def cancelquiz(request):
    clean_session_dict(request)
    return discoverpage(request)

def calcul_success_rate(quiz_results):
    right_answers = 0

    for answer_id in quiz_results:
        if Answer.objects.get(id=answer_id).is_right:
            right_answers += 1

    try:
        success_rate = (right_answers/len(quiz_results)) * 100
    except(ZeroDivisionError):
        success_rate = 0

    return success_rate

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

def get_language(request):
    return request.session.get('lang', 'fr')

def set_language(request, language):
    request.session['lang'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))
