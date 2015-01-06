from django.conf.urls import patterns, url


urlpatterns = patterns(
    'core.views',
    url(r'^$', 'home', name='home'),
    url(r'^alunos$', 'students', name='students'),
)
