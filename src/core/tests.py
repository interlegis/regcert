from django.test import Client, TestCase


class HomeNotAuthenticatedTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get('/')

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response,
                                'core/home_not_authenticated.html')

