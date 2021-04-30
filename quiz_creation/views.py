from django.shortcuts import render, redirect
from quiz_app.models import Quiz, Question, Answer
from django.contrib import messages
from django.http import JsonResponse
import json
import pickle

from django.http import JsonResponse

def createquizpage(request):
    return render(request, "createquiz.html")


# Returns True if any of the args is empty
def is_empty(*args):
    return any([len(str(elt)) < 1 for elt in args])

# Returns True if the question in parameter is already in the quiz
def is_already_in(request, question):
    existing_questions = request.session["current_quiz_creation"]

    if 'question_to_edit' in request.session:
        question_to_edit = request.session["question_to_edit"]
    else:
        question_to_edit = ""

    for qu in existing_questions:
        if question == qu['question']:
            if qu == question_to_edit:
                continue
            return True


def checkfields(request, question, right_answer, answers):

    if is_empty(question, *answers):
        message = "Tous les champs doivent être remplis."
        return ('error', message)

    elif len(right_answer) < 1:
        message = "Il doit y avoir au moins une bonne réponse."
        return ('error', message)

    elif len(answers) != len(set(answers)):
        message = "Il ne peut pas y avoir deux réponses identiques."
        return ('error', message)

    elif is_already_in(request, question):
        message = "Cette question est déjà présente dans votre quiz."
        return ('error', message)

    else:
        return ('all good')


def remove_quotes(string):
    if string[0] == '"' and string[-1] == '"':
        return string[1:-1]


def ajaxcheckquestionfields(request):

    question = remove_quotes(request.GET['question_title'])
    answers = eval(json.loads(request.GET['answers']))
    right_answer = remove_quotes(request.GET['right_answer'])

    are_fields_ok = checkfields(request, question, right_answer, answers)

    if 'error' in are_fields_ok:
        return JsonResponse({'error': are_fields_ok[1]})
    else:
        question_data = {'question': question,
                         'answers': answers,
                         'right_answer': right_answer}


        # Saves the questions in session dict all along the quiz creation
        if "current_quiz_creation" not in request.session:
            request.session["current_quiz_creation"] = []

        request.session["current_quiz_creation"].append(question_data)
        request.session.modified = True

        return JsonResponse(question_data)


def createquiz(request):

    request.session["current_quiz_creation"] = []

    quiz_name = request.POST['quiz_name']
    is_public = eval(request.POST['is_public'])
    difficulty = request.POST['quiz_difficulty']
    language = request.session.get('lang', 'fr')

    quiz = Quiz(title=quiz_name,
                is_public=is_public,
                difficulty=difficulty,
                language=language)

    pickled_quiz = pickle.dumps(quiz)

    str_pickled_quiz = pickled_quiz.decode('latin-1')
    request.session['quiz_infos'] = str_pickled_quiz
    return render(request, "quiz_creation.html", {'quiz': quiz})


def ajaxcheckquiz(request):
    quiz_questions = request.session['current_quiz_creation']
    if len(quiz_questions) < 2:
        message = "Vous devez créer au moins deux questions."
        return JsonResponse({'error': message})
    else:
        return JsonResponse({})


def submitquiz(request):
    quiz_questions = request.session['current_quiz_creation']

    str_pickled_quiz = request.session['quiz_infos']
    bytes_pickled_quiz = str_pickled_quiz.encode('latin-1')

    quiz = pickle.loads(bytes_pickled_quiz)
    quiz.save()
    for elt in quiz_questions:
        question = Question.objects.create(title=elt['question'],
                                           quiz=quiz)

        for answer in elt['answers']:
            if answer == elt['right_answer']:
                Answer.objects.create(title=answer,
                                      question=question,
                                      is_right=True)
            else:
                Answer.objects.create(title=answer,
                                      question=question,
                                      is_right=False)
    print(quiz.id)
    return redirect("/create")


def deletequiz(request):
    if request.method == 'POST':
        try:
            del(request.session['quiz_infos'])
            del(request.session['current_quiz_creation'])
            del(request.session['question_to_edit'])
            request.session.modified = True
        except:
            pass
    return redirect("/")


def ajaxdeletequestion(request):

    question_title = request.GET['question_title']

    for index, question in enumerate(request.session['current_quiz_creation']):

        if question['question'] == question_title:

            del(request.session['current_quiz_creation'][index])
            request.session.modified = True

    return JsonResponse({})

def ajaxgetquestiontoedit(request):

    question_title = request.GET['question_title']
    for index, question in enumerate(request.session['current_quiz_creation']):

        if question['question'] == question_title:
            answers = question['answers']
            request.session['question_to_edit'] = question
            request.session.modified = True

    return JsonResponse({'answers': answers})


def ajaxeditquestion(request):
    question = remove_quotes(request.GET['question_title'])
    answers = json.loads(request.GET['answers'])
    right_answer = remove_quotes(request.GET['right_answer'])

    are_fields_ok = checkfields(request, question, right_answer, answers)

    if 'error' in are_fields_ok:
        return JsonResponse({'error': are_fields_ok[1]})
    else:
        question_to_edit = request.session['question_to_edit']
        for elt in request.session['current_quiz_creation']:
            if elt == question_to_edit:
                elt['question'] = question
                elt['answers'] = answers
                elt['right_answer'] = right_answer

        del(request.session['question_to_edit'])
        request.session.modified = True

    question_data = {'question': question,
                     'answers': answers,
                     'right_answer': right_answer,
                     'ancient_question': question_to_edit['question']}

    return JsonResponse(question_data)


def ajaxremovequestiontoedit(request):
    try:
        del(request.session['question_to_edit'])
        request.session.modified = True
    except:
        pass
    return JsonResponse({})
