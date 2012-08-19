from django.shortcuts import render, redirect

from blogs.forms import BlogForm
from blogs.models import Blog, Source

from repositories.forms import RepoForm

from .utils import get_object_or_None


def home(request):
    blog_source_id = request.session.get('blog_source_id')
    blog_id = request.session.get('blog_id')

    blog_source = get_object_or_None(Source, id=blog_source_id)
    blog = get_object_or_None(Blog, id=blog_id)

    blog_url = getattr(blog, 'domain', '')
    blog_form = BlogForm(blog_source=blog_source)

    return render(request, 'index.html', {
        'repo_form': RepoForm(initial={'name': blog_url}),
        'blog_form': blog_form
    })


def logout(request):
    request.session.pop('blog_id', None)
    request.session.pop('blog_source_id', None)
    request.session.pop('repo_id', None)
    request.session.pop('repo_user_id', None)
    return redirect('home')
