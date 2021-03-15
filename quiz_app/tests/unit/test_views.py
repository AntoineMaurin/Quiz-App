from django.test import TestCase, Client
from quiz_app.models import Quiz, Question

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
