from django.conf.urls import patterns, url
from core.views import (StudentCreate, StudentView, StudentUpdate,
                        StudentDelete, CourseView, CourseCreate, CourseUpdate,
                        CourseDelete, CertificateView)


urlpatterns = patterns(
    'core.views',
    url(r'^$', 'home', name='home'),
    url(r'^alunos$', StudentView.as_view(), name='students'),
    url(r'^alunos/cadastrar$', StudentCreate.as_view(), name='student_create'),
    url(r'^alunos/editar/(?P<pk>[\w-]+)$', StudentUpdate.as_view(),
        name='student_update'),
    url(r'^alunos/remover/(?P<pk>[\w-]+)$', StudentDelete.as_view(),
        name='student_delete'),
    url('^cursos$', CourseView.as_view(), name='courses'),
    url('^cursos/cadastrar$', CourseCreate.as_view(), name='course_create'),
    url(r'^cursos/editar/(?P<pk>[\w-]+)$', CourseUpdate.as_view(),
        name='course_update'),
    url(r'^cursos/remover/(?P<pk>[\w-]+)$', CourseDelete.as_view(),
        name='course_delete'),
    url(r'^certificados$', CertificateView.as_view(), name='certificates'),
)


