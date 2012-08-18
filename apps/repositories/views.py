from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RepoForm
from .models import User, Repo
from .utils import get_access_data, get_user_info


def oauth2callback(request):
    query_params = request.GET.copy()
    query_code = query_params.get('code', None)
    if not query_code:
        return auth_failed(request, 'Did not receive code in query string!')

    access_data = get_access_data(query_code)
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


def save_repo(request):
    repositories_user = request.session.get('repositories_user')
    form = RepoForm(
        repositories_user=repositories_user,
        data=request.POST
    )
    form_valid = form.is_valid()
    if form_valid:
        blog = request.session.get('blog')
        obj, created = Repo.objects.get_or_create(
            user=repositories_user, blog=blog, name=form['name'].value(),
            cname=form['cname'].value()
        )
        request.session['repo'] = obj
        request.session.modified = True

    return render(request, 'repositories/save_repo.html', {
        'repo_form': form,
        'form_valid': form_valid
    })