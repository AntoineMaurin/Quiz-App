from django.shortcuts import render
from Quiz_App.models import Quiz, Question, Answer

def homepage(request):
    return render(request, "home.html")

def portalpage(request):
    return render(request, "portal.html")

def createquizpage(request):
    return render(request, "createquiz.html")

def startquiz(request):
    if request.method == 'POST':
        quiz_name = request.POST['quiz_name']
        quiz = Quiz.objects.create(title=quiz_name)
    return render(request, "quiz_question.html", {'quiz': quiz})

def addquestion(request):
    if request.method == 'POST':
        quiz_id = request.POST['quiz_id']
        question_text = request.POST['question_text']
        ans1 = request.POST['ans1']
        ans2 = request.POST['ans2']
        ans3 = request.POST['ans3']
        ans4 = request.POST['ans4']

        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.create(title=question_text,
                                           quiz=quiz)
        Answer.objects.create(title=ans1, question=question, is_right=True)
        Answer.objects.create(title=ans2, question=question, is_right=False)
        Answer.objects.create(title=ans3, question=question, is_right=False)
        Answer.objects.create(title=ans4, question=question, is_right=False)

    return render(request, "quiz_question.html", {'quiz': quiz})

def submitquiz(request):
    print('ez clap, votre quizz est créé !')
    return render(request, "createquiz.html")
