from django.conf.urls import patterns, url

from certificate.views import (CertificateCreate, CertificateList,
                               CertificateDetail, CertificateValidate,
                               CertificateInvalidate, CertificateSearch)


urlpatterns = patterns(
    'certificate.views',
    url(r'^$', CertificateList.as_view(), name='certificate_list'),
    url(r'^adicionar$', CertificateCreate.as_view(),
        name='certificate_create'),
    url(r'^detalhes/(?P<pk>[\w-]+)$',
        CertificateDetail.as_view(), name='certificate_detail'),
    url(r'^validar/(?P<verification_code>[\w-]+)$',
        CertificateValidate.as_view(), name='certificate_validate'),
    url(r'^invalidar/(?P<pk>[\w-]+)$',
        CertificateInvalidate.as_view(), name='certificate_invalidate'),
    url(r'^buscar$', CertificateSearch.as_view(),
        name='certificate_search'),
)
