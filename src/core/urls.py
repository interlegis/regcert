from django.conf.urls import patterns, url
from core.views import (Home, StudentCreate, StudentView, StudentUpdate,
                        CourseView, CourseCreate, CourseUpdate,
                        CertificateView, CertificateCreate,
                        CertificateInvalidate,
                        CertificateDetail, CertificateValidate,
                        CertificateSearch)


urlpatterns = patterns(
    'core.views',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^alunos$', StudentView.as_view(), name='students'),
    url(r'^alunos/cadastrar$', StudentCreate.as_view(), name='student_create'),
    url(r'^alunos/editar/(?P<pk>[\w-]+)$', StudentUpdate.as_view(),
        name='student_update'),
    url('^cursos$', CourseView.as_view(), name='courses'),
    url('^cursos/cadastrar$', CourseCreate.as_view(), name='course_create'),
    url(r'^cursos/editar/(?P<pk>[\w-]+)$', CourseUpdate.as_view(),
        name='course_update'),
    url(r'^certificados$', CertificateView.as_view(), name='certificates'),
    url(r'^certificados/cadastrar$', CertificateCreate.as_view(),
        name='certificate_create'),
    url(r'^certificados/validar/(?P<validation_code>[\w-]+)$',
        CertificateValidate.as_view(), name='certificate_validate'),
    url(r'^certificados/buscar$', CertificateSearch.as_view(),
        name='certificate_search'),
    url(r'^certificados/detalhes/(?P<pk>[\w-]+)$', CertificateDetail.as_view(),
        name='certificate_detail'),
    url(r'^certificados/invalidar/(?P<pk>[\w-]+)$',
        CertificateInvalidate.as_view(), name='certificate_invalidate'),
)
