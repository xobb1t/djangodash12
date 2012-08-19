from django.conf.urls import url, patterns


urlpatterns = patterns(
    'blogs.views',
    url(r'^oauth2callback$', 'oauth2callback', name='blogs_oauth2callback'),
    url(r'^blog/add/$', 'blog_form', name='blogs_blog_add'),
)
