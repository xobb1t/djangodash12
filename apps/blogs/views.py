from datetime import datetime, timedelta
import requests

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

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
    expiration_datetime = datetime.now() + timedelta(data['expires_in'])
    defaults = {
        'username': user_info['email'],
        'access_token': data['access_token'],
        'expiration_datetime': expiration_datetime,
    }

    source, created = Source.objects.create_or_update(
        identificator=blog_info['id'], defaults=defaults
    )
    request.session['blog_source'] = source
    return redirect('home')


def authorization_failed(request):
    messages.error(request, 'Something went wrong, you are not authorized')
    return redirect('home')
