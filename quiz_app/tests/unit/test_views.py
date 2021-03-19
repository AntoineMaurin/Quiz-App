from quiz_app.views import calcul_success_rate
from django.test import TestCase, Client
from quiz_app.models import Quiz, Question, Answer

class QuizAppViewsTest(TestCase):

    fixtures = ['quiz_data.json']

    def setUp(self):
        self.client = Client()

        #Takes the first quiz of all in the test database
        self.quiz = Quiz.objects.all()[:1][0]
        self.questions = Question.objects.filter(quiz=self.quiz)

    def test_discoverpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discoverpage.html')
        self.assertIn('quizzes', response.context)
        for quiz in response.context['quizzes']:
            self.assertTrue(quiz.is_public)

    def test_playpage(self):
        response = self.client.get('/play')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'play.html')

    def test_startquizpage(self):
        response = self.client.get('/startquiz/' + str(self.quiz.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome_quiz.html')
        self.assertIn('quiz', response.context)
        self.assertEqual(response.context['quiz'], self.quiz)
        self.assertEqual(len(self.client.session['questions_left']),
                         len(self.questions))
        for question in self.questions:
            self.assertIn(question.id, self.client.session['questions_left'])

    def test_startquizpage_with_quiz_that_doesnt_exist(self):
        response = self.client.get('/startquiz/39175475872')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discoverpage.html')

    def test_startquizpage_with_play_form(self):
        response = self.client.get('/startquiz/0', {'quiz_id': self.quiz.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'welcome_quiz.html')
        self.assertEqual(response.context['quiz'], self.quiz)

    def test_nextquestionpage(self):
        self.client.get('/startquiz/' + str(self.quiz.id))
        response = self.client.get('/nextquestion')
        self.assertEqual(response.status_code, 200)

    def test_calcul_success_rate_all_right(self):
        all_questions = Question.objects.filter(quiz=self.quiz)
        answers = []
        for question in all_questions:
            current_question_answers = Answer.objects.filter(question=question)
            answers.append(tuple(current_question_answers))

        test_quiz_results = []
        for index, elt in enumerate(all_questions):
            for answer in answers[index]:
                if answer.is_right:
                    test_quiz_results.append([elt, [answer.id]])

        success_rate = calcul_success_rate(test_quiz_results, self.quiz)
        self.assertEqual(success_rate, 100.0)
