from django.conf.urls import patterns, url

from reports.views import (ReportsView, ReportAllValidCertificates,
                           ReportAllCertificates, ReportCertificatesByCourse,
                           ReportCertificatesByDate)


urlpatterns = patterns(
    'reports.views',
    url(r'^$', ReportsView.as_view(),
        name='reports'),
    url(r'^certificados/todos$', ReportAllCertificates.as_view(),
        name='report_all_certificates'),
    url(r'^certificados/validos$', ReportAllValidCertificates.as_view(),
        name='report_all_valid_certificates'),
    url(r'^certificados/curso/(?P<course_name>[\w-]+)$',
        ReportCertificatesByCourse.as_view(),
        name='report_certificates_by_course'),
    url(r'^certificados/data/(?P<date>\d{2}-\d{2}-\d{4})$',
        ReportCertificatesByDate.as_view(),
        name='report_certificates_by_date'),
)
