from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import oauth2callback, save_repo


urlpatterns = patterns(
    '',
    url(r'^oauth2callback/$', oauth2callback,
        name='repositories_oauth2callback'),
    url(r'^save_repo/$', save_repo, name='repositories_save_repo'),
)
