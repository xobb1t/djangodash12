from datetime import datetime, timedelta
import requests

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Source
from .utils import get_tokens, AuthError, blogger_resource


def oauth2callback(request):
    kwargs = request.GET.copy()
    if kwargs.get('error') or not kwargs.get('code'):
        return authorization_failed(request)
    try:
        data = get_tokens(kwargs.get('code'))
    except AuthError:
        return authorization_failed(request)
    user_info = blogger_resource(
        resource='users/self',
        access_token=data['access_token'],
    )
    expiration_datetime = datetime.now() + timedelta(data['expires_in'])
    defaults = {
        'username': user_info.get('displayName', ''),
        'access_token': data['access_token'],
        'expiration_datetime': expiration_datetime,
    }
    source, created = Source.objects.create_or_update(
        user_id=user_info['id'], defaults=defaults
    )
    request.session['source_id'] = source.pk
    return HttpResponse()


def authorization_failed(request):
    messages.error(request, 'Something went wrong, you are not authorized')
    return redirect('home')
