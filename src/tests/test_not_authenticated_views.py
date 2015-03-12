from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import Client
import pytest
from model_mommy import mommy

from certificate.models import Certificate, InvalidCertificate


def _test_not_authenticated_request(url_pattern, **kwargs):
    client = Client()
    prefix = 'http://testserver/login?next=/'

    response = client.get(reverse(url_pattern, kwargs=kwargs), follow=True)

    redirect_url, status_code = response.redirect_chain[0]

    assert len(response.redirect_chain) == 1
    assert response.status_code == 200
    assert redirect_url.startswith(prefix) == True
    assert status_code == 302


# Certificate - views.py

def test_certificate_list_view():
    _test_not_authenticated_request('certificate_list')


def test_certificate_create_view():
    _test_not_authenticated_request('certificate_create')


@pytest.mark.django_db
def test_certificate_detail_view():
    mommy.make(Certificate, id=1)
    _test_not_authenticated_request('certificate_detail', **{'pk': 1})


@pytest.mark.django_db
def test_certificate_invalidate_view():
    mommy.make(InvalidCertificate, pk=1)
    _test_not_authenticated_request('certificate_invalidate',
                                    **{'pk': 1})


def test_certificate_search_view():
    _test_not_authenticated_request('certificate_search')


# Report - views.py

def test_report_all_certificates_view():
    _test_not_authenticated_request('report_all_certificates')


def test_report_all_valid_certificates_views():
    _test_not_authenticated_request('report_all_valid_certificates')


def test_report_all_invalid_certificates_view():
    _test_not_authenticated_request('report_all_invalid_certificates')


@pytest.mark.django_db
def test_report_certificates_by_course_view():
    mommy.make(Certificate, course_name='test course')
    _test_not_authenticated_request('report_certificates_by_course',
                                    **{'course_name': 'test-course'})


@pytest.mark.django_db
def test_report_certificates_by_date_view():
    date = datetime.now()
    mommy.make(Certificate, verification_code_date_time=date)
    date_param = '{}-{}-{}'.format(date.day, date.month, date.year)
    _test_not_authenticated_request('report_certificates_by_date',
                                    **{'date': date_param})


@pytest.mark.django_db
def test_report_certificates_by_book_date_view():
    date = datetime.now()
    mommy.make(Certificate, book_date=date)
    date_param = '{}-{}-{}'.format(date.day, date.month, date.year)
    _test_not_authenticated_request('report_certificates_by_book_date',
                                    **{'date': date_param})
