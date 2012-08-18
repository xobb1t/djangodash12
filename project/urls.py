from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='base.html'
    ), name='home'),
    url(r'^blogs/', include('blogs.urls')),
    url(r'^repositories/', include('repositories.urls')),
)
