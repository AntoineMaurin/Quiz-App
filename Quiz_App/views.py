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

    try:
        current_question_id = request.session['questions_left'][0]
        current_question = Question.objects.get(id=current_question_id)
        answers = Answer.objects.filter(question=current_question)
        quiz_id = request.session['quiz_id']

        quiz = Quiz.objects.get(id=quiz_id)

        request.session['question_number'] += 1
        del(request.session['questions_left'][0])
        request.session.modified = True

        return render(request, "quiz_question_playing.html", {'quiz': quiz,
                                                              'current_question': current_question,
                                                              'answers': answers,
                                                              'question_number': request.session['question_number'],
                                                              })
    except(IndexError):
        return render(request, "results.html")

def questionresultspage(request):

    if request.method == 'POST':
        checked_answers = request.POST.getlist('is_answer_checked')

        answered_question_id = request.session['questions_left'][0]
        answered_question = Question.objects.get(id=answered_question_id)
        all_answers = Answer.objects.filter(question=answered_question)

        return render(request, "question_results.html",
        {'checked_answers': checked_answers,
         'answered_question': answered_question,
         'all_answers': all_answers})
