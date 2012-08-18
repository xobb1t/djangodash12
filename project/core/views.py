from django.shortcuts import render

from blogs.forms import BlogForm

from repositories.forms import RepoForm


def home(request):
    blog_source = request.session.get('blog_source')
    if blog_source and not blog_source.is_expired:
        blog_form = BlogForm(token=blog_source.access_token)
    else:
        blog_form = None
    return render(request, 'index.html', {
        'repo_form': RepoForm, 'blog_form': blog_form
    })
