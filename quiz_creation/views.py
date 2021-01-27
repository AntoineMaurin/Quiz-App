from django.shortcuts import render
from Quiz_App.models import Quiz, Question, Answer
from django.contrib import messages

from django.http import JsonResponse

def createquizpage(request):
    if request.method == 'POST':
        quiz_id = request.session['quiz_id']
        messages.success(request, f'Your quiz code is {quiz_id}')
        return render(request, "discoverpage.html")
    else:
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
        request.session['quiz_id'] = quiz.id
    return render(request, "quiz_question_form.html", {'quiz': quiz})

def addquestion(request):
    if request.method == 'POST':
        quiz_id = request.session['quiz_id']
        question_text = request.POST['question_text']
        answers = request.POST.getlist('answer')
        right_answers = request.POST.getlist('is_ans_right')

        quiz = Quiz.objects.get(id=quiz_id)

        fields_to_check = answers + [question_text]

        fields_are_good = treat_fields(fields_to_check, right_answers)

        if not fields_are_good:
            messages.error(request, 'The question and the answer fields '
            'have to be completed.')
            return render(request, "quiz_question_form.html", {'quiz': quiz})

        question = Question.objects.create(title=question_text,
                                           quiz=quiz)

        bind_answers_to_question(answers, right_answers, question)

        return render(request, "quiz_question_form.html", {'quiz': quiz})


def submitquiz(request):
    if request.method == 'POST':
        quiz_id = request.session['quiz_id']
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        return render(request, "quiz_building_summary.html", {'quiz': quiz,
                                                              'questions': questions})

def deletequestion(request, index):
    if request.POST:
        quiz_id = request.session['quiz_id']
        quiz = Quiz.objects.get(id=quiz_id)

        questions = Question.objects.filter(quiz=quiz)

        question = questions[index]
        question.delete()

        return render(request, "quiz_building_summary.html", {'quiz': quiz,
                                                              'questions': questions})
    else:
        return render(request, "createquiz.html")


"""The process of question edition is :
-First, identify which question is being edited with its index.
-Second, get the data from the edition form (same fields as the question
creation form).
-Third, replace the question text and its answers. For the answers, all the
ancient answers are deleted before the new ones are added."""
def editquestion(request, index):
    if request.POST:
        quiz_id = request.session['quiz_id']
        quiz = Quiz.objects.get(id=quiz_id)

        questions = Question.objects.filter(quiz=quiz)

        question_to_edit = questions[index]

        question_text = request.POST['question_text']
        new_answers = request.POST.getlist('answer')
        right_answers = request.POST.getlist('is_ans_right')

        question_to_edit.title = question_text
        question_to_edit.save()

        Answer.objects.filter(question=question_to_edit).delete()

        bind_answers_to_question(new_answers, right_answers, question_to_edit)

        return render(request,
                     "quiz_building_summary.html",
                     {'quiz': quiz,
                      'questions': questions})
    else:
        return render(request, "createquiz.html")


"""Gets via ajax the index of the question to edit. Then returns a list of
tuples where the first element is the answer text, and the second a boolean
that tells if the answer is right or not."""
def ajaxgetanswers(request):
    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)

    index = request.GET['question_index']
    index = int(index)

    questions = Question.objects.filter(quiz=quiz)
    question = questions[index]

    answers = Answer.objects.filter(question=question)

    data = []
    for answer in answers:
        data.append((answer.title, answer.is_right))

    return JsonResponse(data, safe=False)


def deletequiz(request):
    quiz_id = request.session['quiz_id']
    Quiz.objects.get(id=quiz_id).delete()
    return render(request, "createquiz.html")



def bind_answers_to_question(answers_titles, right_answers, question):
    for answer in answers_titles:
        if answer in right_answers:
            Answer.objects.create(title=answer, question=question, is_right=True)
        else:
            Answer.objects.create(title=answer, question=question, is_right=False)


"""Returns a boolean. Returns False if all the fields are not filled and if
there is no right answer checked."""
def treat_fields(fields_list, right_answers):
    if len(right_answers) < 1:
        return False
    for field in fields_list:
        if len(field) < 1:
            return False
    return True
