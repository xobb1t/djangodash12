from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import oauth2callback


urlpatterns = patterns(
    '',
    url(r'^oauth2callback/$', oauth2callback,
        name='repositories_oauth2callback'
    ),
    url(r'^login/$', 
        TemplateView.as_view(
            template_name='repositories/login.html'
        ), 
        name='repositories_login'
    ),
)
