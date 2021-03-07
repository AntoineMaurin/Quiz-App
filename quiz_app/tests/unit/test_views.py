from django.test import TestCase, Client

class AppViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_discoverpage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discoverpage.html')
        self.assertIn('quizzes', response.context)

    def test_playpage(self):
        response = self.client.get('/play')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'play.html')
