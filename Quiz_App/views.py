from django.shortcuts import render
from Quiz_App.models import Quiz, Question, Answer
from django.contrib import messages

from django.http import JsonResponse


def discoverpage(request):
    quizzes = Quiz.objects.filter(is_public=True)
    return render(request, "discoverpage.html", {'quizzes': quizzes})

def playpage(request):
    return render(request, "play.html")

def createquizpage(request):
    return render(request, "createquiz.html")

def questioncreationpage(request):
    if request.method == 'POST':
        quiz_name = request.POST['quiz_name']
        is_public = request.POST['is_public']
        if is_public == 'True':
            is_public = True
        else:
            is_public = False
        quiz = Quiz.objects.create(title=quiz_name,
                                   is_public=is_public)
    return render(request, "quiz_question_form.html", {'quiz': quiz})

def addquestion(request):
    if request.method == 'POST':
        quiz_id = request.POST['quiz_id']
        question_text = request.POST['question_text']
        ans1 = request.POST['ans1']
        ans2 = request.POST['ans2']

        quiz = Quiz.objects.get(id=quiz_id)

        fields_to_check = [question_text, ans1, ans2]

        for field in fields_to_check:
            if len(field) < 1:
                messages.error(request, 'The question and at least two '
                'answers have to be completed.')
                return render(request, "quiz_question_form.html", {'quiz': quiz})

        ans1_is_right = True if 'ans1_is_right' in request.POST else False
        ans2_is_right = True if 'ans2_is_right' in request.POST else False

        if not ans1_is_right and not ans2_is_right:
            messages.error(request, 'The question needs to have at least one '
            'right answer.')
            return render(request, "quiz_question_form.html", {'quiz': quiz})

        question = Question.objects.create(title=question_text,
                                           quiz=quiz)

        answer_1 = Answer.objects.create(title=ans1, question=question, is_right=ans1_is_right)
        answer_2 = Answer.objects.create(title=ans2, question=question, is_right=ans2_is_right)


        return render(request, "quiz_question_form.html", {'quiz': quiz})

def submitquiz(request):
    if request.method == 'POST':
        quiz_id = request.POST['quiz_id']
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        return render(request, "quiz_building_summary.html", {'quiz': quiz,
                                                              'questions': questions})

def startquizpage(request):
    id = request.GET['quiz_id']
    quiz = Quiz.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)
    ids_list = []
    for question in questions:
        ids_list.append(question.id)
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

        del(request.session['questions_left'][0])
        request.session.modified = True

        return render(request, "quiz_question_playing.html", {'quiz': quiz,
                                                              'current_question': current_question,
                                                              'ans1': answers[0],
                                                              'ans2': answers[1],
                                                              })
    except(IndexError):
        return render(request, "results.html")


def deletequestion(request):
    if request.POST:
        question_id = request.POST['question_id']

        print(question_id)

        question = Question.objects.get(id=question_id)
        quiz = question.quiz
        questions = Question.objects.filter(quiz=quiz)

        Question.objects.get(id=question_id).delete()

        return render(request, "quiz_building_summary.html", {'quiz': quiz,
                                                              'questions': questions})
