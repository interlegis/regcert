from django.conf.urls import patterns, url

from reports.views import ReportAllCertificates


urlpatterns = patterns(
    'reports.views',
    url(r'^certificados$', ReportAllCertificates.as_view(),
        name='report_all_certificates'),
)
