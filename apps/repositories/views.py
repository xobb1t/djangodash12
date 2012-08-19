from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from blogs.models import Blog
from project.core.utils import get_object_or_None

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

    request.session['repo_user_id'] = user_obj.pk
    return redirect('home')


def auth_failed(request, error_msg):
    messages.error(request, error_msg)
    return redirect('home')


def save_repo(request):
    repo_user_id = request.session.get('repo_user_id')
    repo_user = get_object_or_None(User, pk=repo_user_id)
    blog_id = request.session.get('blog_id')
    blog = get_object_or_None(Blog, pk=blog_id)
    if not all((blog, repo_user)):
        raise Http404

    form = RepoForm(
        repo_user=repo_user,
        data=request.POST
    )
    if form.is_valid():
        name = form.cleaned_data['name']
        cname = form.cleaned_data.get('cname', '')
        repo, created = Repo.objects.get_or_create(
            user=repo_user, blog=blog,
            name=name, cname=name
        )
        request.session['repo_id'] = repo.pk
        return render(request, 'repositories/repository_saved.html', {
            'repo': repo
        })

    return render(request, 'repositories/repository_form.html', {
        'form': form,
    })
