from django.conf.urls import patterns, url

from reports.views import ReportAllValidCertificates, ReportAllCertificates


urlpatterns = patterns(
    'reports.views',
    url(r'^certificados_validos$', ReportAllValidCertificates.as_view(),
        name='report_all_certificates'),
    url(r'^todos_certificados$', ReportAllCertificates.as_view(),
        name='report_all_certificates'),
)
