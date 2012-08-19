from django.http import HttpResponse
from django.shortcuts import get_object_or_None

from blogs.models import Blog
from repo.models import Repo

from .models import Process
from .tasks import work_on


def start_import(request):
    blog_id = request.session.get('blog_id')
    blog = get_object_or_404(Blog, pk=blog_id)

    repo_id = request.session.get('repo_id')
    repo = get_object_or_404(Repo, pk=repo_id)

    process, created = Process.objects.get_or_create(
        blog=blog, process=process, defaults={
            'stage': 1,
        }
    )
    if created:
        work_on.delay(process)
    return HttpResponse(process.stage)
