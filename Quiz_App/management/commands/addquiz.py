from django.core.management.base import BaseCommand
from Quiz_App.models import Quiz, Question, Answer
import requests
import json

class Command(BaseCommand):

    help = """"""

    def add_arguments(self, parser):
        parser.add_argument('quiz_url')

    def handle(self, *args, **options):
        url_to_use = options['quiz_url']
        url = url_to_use
        response = requests.get(url)
        title = response.json()['thème']

        quiz_dict = response.json()['quizz']['fr']

        easy_quiz = self.create_quiz(title, "easy")
        medium_quiz = self.create_quiz(title, "medium")
        hard_quiz = self.create_quiz(title, "hard")

        for question_dict in quiz_dict['débutant']:
            self.build_quiz(question_dict, easy_quiz)

        for question_dict in quiz_dict['confirmé']:
            self.build_quiz(question_dict, medium_quiz)

        for question_dict in quiz_dict['expert']:
            self.build_quiz(question_dict, hard_quiz)

    def build_quiz(self, data, empty_quiz):
        question_text = data['question']
        answers_list = data['propositions']
        right_answer = data['réponse']

        question = self.add_questions(empty_quiz, question_text)
        self.add_answers(answers_list, right_answer, question)

    def create_quiz(self, title, difficulty):
        quiz = Quiz.objects.create(title=title,
                                   is_public=True,
                                   difficulty=difficulty)
        return quiz

    def add_questions(self, quiz, question_text):

        question = Question.objects.create(title=question_text,
                                           quiz=quiz)

        return question

    def add_answers(self, answers_list, right_answer, question):
        for answer in answers_list:
            if answer == right_answer:
                is_right = True
            else:
                is_right = False
            Answer.objects.create(title=answer,
                                  question=question,
                                  is_right=is_right)
