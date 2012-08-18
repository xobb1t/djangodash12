from django.shortcuts import render

from repositories.forms import RepoForm

def home(request):
    return render(request, 'index.html', {'repo_form': RepoForm})
