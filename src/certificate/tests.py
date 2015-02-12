from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy

from certificate.models import Certificate


class NotAuthenticatedTestCase(TestCase):

    def setUp(self):
        self.certificate = mommy.make(Certificate, id=1)

    def _test_request(self, pattern_name, redirect_url='', **kwargs):
        response = self.client.get(reverse(pattern_name, kwargs=kwargs),
                                   follow=True)
        prefix = 'http://testserver/login?next=/'
        response_redirect_url = response.redirect_chain[0][0]
        response_status_code = response.redirect_chain[0][1]

        self.assertEqual(len(response.redirect_chain), 1)
        self.assertTrue(response_status_code, 302)
        self.assertTrue(response_redirect_url.startswith(prefix))

    def test_certificate_list_view(self):
        self._test_request('certificate_list')

    def test_certificate_create_view(self):
        self._test_request('certificate_create')

    def test_certificate_detail_view(self):
        self._test_request('certificate_detail', **{'pk': 1})

    def test_certificate_validate_view(self):
        self._test_request('certificate_invalidate', **{'pk': 1})

    def test_certificate_search_view(self):
        self._test_request('certificate_search')
