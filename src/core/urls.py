from django.conf.urls import patterns, url
from core.views import StudentCreate, StudentView


urlpatterns = patterns(
    'core.views',
    url(r'^$', 'home', name='home'),
    url(r'^alunos/cadastrar$', StudentCreate.as_view(), name='student_create'),
    url(r'^alunos$', StudentView.as_view(), name='students'),
)
