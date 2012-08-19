import requests

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from project.core.utils import get_object_or_None

from .forms import BlogForm
from .models import Source
from .utils import get_tokens, AuthError, api_resource


def oauth2callback(request):
    kwargs = request.GET.copy()
    if kwargs.get('error') or not kwargs.get('code'):
        return authorization_failed(request)
    try:
        data = get_tokens(kwargs.get('code'))
    except AuthError:
        return authorization_failed(request)

    blog_info = api_resource(
        root=settings.BLOGGER_API_ROOT,
        resource='users/self',
        access_token=data['access_token'],
    )
    user_info = api_resource(
        root=settings.GOOGLE_API_ROOT,
        resource='userinfo',
        access_token=data['access_token'],
    )
    expires_in = timedelta(seconds=data['expires_in'])
    expiration_datetime = datetime.now() + expires_in
    defaults = {
        'username': user_info['email'],
        'access_token': data['access_token'],
        'expiration_datetime': expiration_datetime,
    }

    source, created = Source.objects.create_or_update(
        identificator=blog_info['id'], defaults=defaults
    )
    request.session['blog_source_id'] = source.pk
    return redirect('home')


def blog_form(request):
    blog_source_id = request.session.get('blog_source_id')
    blog_source = get_object_or_None(Source, pk=blog_source_id)
    if blog_source is None or blog_source.is_expired:
        raise Http404

    form = BlogForm(blog_source=blog_source, data=request.POST)
    if form.is_valid():
        blog = form.save()
        if blog is not None:
            request.session['blog_id'] = blog.pk
        return render(request, 'blogs/blog_saved.html', {
            'blog': blog
        })
    return render(request, 'blogs/blog_form.html', {
        'form': form
    })


def authorization_failed(request):
    messages.error(request, 'Something went wrong, you are not authorized')
    return redirect('home')
