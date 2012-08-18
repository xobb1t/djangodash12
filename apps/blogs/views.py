import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .utils import get_tokens, AuthError


def oauth2callback(request):
    kwargs = request.GET.copy()
    if kwargs.get('error') or not kwargs.get('code'):
        return authorization_faield(request)
    try:
        access_token, refresh_token, lifetime = get_tokens(kwargs.get('code'))
    except AuthError:
        return authorization_faield(request)
    
    return HttpResponse(r.content)


def authorization_faield(request):
    messages.error('Something went wrong, you are not authorized')
    return redirect('home')
