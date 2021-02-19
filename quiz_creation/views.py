from django.shortcuts import render
from quiz_app.models import Quiz, Question, Answer
from django.contrib import messages

from django.http import JsonResponse

def createquizpage(request):
    return render(request, "createquiz.html")

def questioncreationpage(request):
    if 'quiz_id' in request.session:
        try:
            quiz = Quiz.objects.get(id=request.session['quiz_id'])
        except(Quiz.DoesNotExist):
            del(request.session['quiz_id'])
            request.session.modified = True

    if request.method == 'POST':
        quiz_name = request.POST['quiz_name']
        is_public = request.POST['is_public']
        difficulty = request.POST['quiz_difficulty']
        if is_public == 'True':
            is_public = True
        else:
            is_public = False
        quiz = Quiz.objects.create(title=quiz_name,
                                   is_public=is_public,
                                   difficulty=difficulty)
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

        fields_are_good = are_fields_good(fields_to_check)

        if not fields_are_good:
            messages.error(request, 'All visible fields must be completed, '
            'and must not exceed 254 characters.')
            return render(request, "quiz_question_form.html", {'quiz': quiz})

        if len(right_answers) < 1:
            messages.error(request, 'There must be at least one right answer.')
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

def validate_quiz(request):
    quiz_id = request.session['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    if len(questions) < 1:
        messages.error(request, 'Your quiz must have at least one question.')
        return render(request, "quiz_building_summary.html", {'quiz': quiz,
                                                              'questions': questions})
    else:
        del(request.session['quiz_id'])
        request.session.modified = True
        messages.success(request, 'Your quiz had been successfully created ! '
                                  'your quiz code is {}'.format(quiz_id))
        return render(request, "play.html")


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

def ajaxcheckfields(request):
    answers_titles = request.GET.getlist('answers_titles[]')
    answers_types = request.GET.getlist('answers_types[]')

    answers_are_filled = are_fields_good(answers_titles)

    result = {}

    if not answers_are_filled:
        result['error'] = 'answers not filled'
        return JsonResponse(result, safe=False)

    if 'true' in answers_types:
        result['error'] = 'all good'
    else:
        result['error'] = 'no right answer'

    return JsonResponse(result, safe=False)

def deletequiz(request):
    if request.POST:
        quiz_id = request.session['quiz_id']
        Quiz.objects.get(id=quiz_id).delete()
        del(request.session['quiz_id'])
        request.session.modified = True
    return render(request, "createquiz.html")


def bind_answers_to_question(answers_titles, right_answers, question):
    for answer in answers_titles:
        if answer in right_answers:
            Answer.objects.create(title=answer, question=question, is_right=True)
        else:
            Answer.objects.create(title=answer, question=question, is_right=False)


"""Returns a boolean. Returns False if all the fields are not filled and if
there is no right answer checked."""
def are_fields_good(fields_list):
    for field in fields_list:
        if len(field) < 1:
            return False
        elif len(field) > 254:
            return False
    return True
