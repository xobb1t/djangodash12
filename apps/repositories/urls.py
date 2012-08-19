from django.conf.urls import patterns, url

from .views import oauth2callback, save_repo


urlpatterns = patterns(
    '',
    url(r'^oauth2callback/$', oauth2callback,
        name='repositories_oauth2callback'),
    url(r'^save_repo/$', save_repo, name='repositories_save_repo'),
)
