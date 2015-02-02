from django.conf.urls import patterns, url

from core.views import Home


urlpatterns = patterns(
    'core.views',
    url(r'^$', Home.as_view(), name='home'),
)
