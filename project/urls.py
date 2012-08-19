from django.conf.urls import patterns, include, url

from core.views import home

urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^parser/', include('parser.urls')),
    url(r'^repositories/', include('repositories.urls')),
)
