from django.contrib import messages
from django.shortcuts import redirect

from .models import User
from .utils import get_access_data, get_user_info


def oauth2callback(request):
    query_params = request.GET.copy()
    query_code = query_params.get('code', None)
    if not query_code:
        return auth_failed(request, 'Did not receive code in query string!')

    access_data = get_access_data(code)
    access_token = access_data.get('access_token', None)
    if not access_token:
        return auth_failed(request, 'Did not receive access token!')

    identification, username = get_user_info(access_token)
    if not identification or not username:
        return auth_failed(request, 'Did not receive user info!')

    user_obj, created = User.objects.get_or_create(
        identification=identification,
        defaults={
            'access_token': access_token,
            'username': username
        }
    )
    if not created:
        user_obj.access_token = access_token
        user_obj.username = username
        user_obj.save()

    request.session['repositories_user'] = user_obj
    request.session.modified = True
    return redirect('home')


def auth_failed(request, error_msg):
    messages.error(request, error_msg)
    return redirect('home')
