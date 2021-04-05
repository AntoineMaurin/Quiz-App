from django.test import TestCase, Client
from quiz_app.models import Quiz, Question

class QuizAppViewsTest(TestCase):

    fixtures = ['quiz_data.json']

    def setUp(self):
        self.client = Client()

        #Takes the first quiz of all in the test database
        self.quiz = Quiz.objects.all()[:1][0]
        self.questions = Question.objects.filter(quiz=self.quiz)

    def test_nextquestionpage_redirects_correctly_while_questions(self):
        self.client.get('/startquiz/' + str(self.quiz.id))
        response = self.client.get('/nextquestion')
        # While there are questions in self.client.session['questions_left']
        while len(self.client.session['questions_left']) < 0:
            response = self.client.post('/nextquestion',
                                       {'checked_answer': ['a wrong answer']})
            self.assertTemplateUsed(response, 'quiz_question_playing.html')

    def test_nextquestionpage_redirects_correctly_whith_questions_left(self):
        self.client.get('/startquiz/' + str(self.quiz.id))
        self.client.get('/nextquestion')
        # Emptying the list at self.client.session['questions_left']
        for _ in self.client.session['questions_left']:
            response = self.client.post('/nextquestion',
                                       {'checked_answer': 'a wrong answer'})
        self.assertTemplateUsed(response, 'quiz_results.html')

    def test_cancel_quiz_deletes_keys(self):
        self.client.get('/startquiz/' + str(self.quiz.id))
        self.client.post('/nextquestion',
                                   {'checked_answer': ['a wrong answer']})
        self.assertEqual(self.client.session['quiz_id'], self.quiz.id)

        self.client.post('/cancelquiz')
        self.assertNotIn('quiz_id', self.client.session)
        self.assertNotIn('quiz_results', self.client.session)
