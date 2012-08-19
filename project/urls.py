from django.conf.urls import patterns, include, url

from project.core.views import home, logout


urlpatterns = patterns(
    '',
    url(r'^$', home, name='home'),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^parser/', include('parser.urls')),
    url(r'^repositories/', include('repositories.urls')),
    url(r'^logout/$', logout, name='logout'),
)
