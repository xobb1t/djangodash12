from django.conf.urls import patterns, url

from .views import oauth2callback


urlpatterns = patterns(
    '',
    url(r'^oauth2callback/$', oauth2callback,
        name='repositories_oauth2callback'),
)
