import os

from celery.task import task
from django.conf import settings

from repositories import utils as repo_utils
from .utils import parse_blog_posts, create_pelican_configs


def exception_handle(func):
    def decorator(process):
        try:
            func(process)
        except Exception, e:
            process.error = '%s: %s' % (e.__class__.__name__, unicode(e))
            process.save()
    decorator.__name__ = func.__name__
    return decorator


@task
def work_on(process):
    process.stage = 'start'

    blog = process.blog
    repo = process.repo

    # Create pelican environemnt
    create_pelican_configs(process)
    parse_blog_posts(process, settings.PARSE_PAGES_COUNT)

    public_key_path = os.path.join(settings.KEYS_ROOT, 'id_rsa.pub')
    with open(public_key_path) as f:
        public_key = f.read()
    repo_utils.git_init_repo(process.path)
    repo_utils.git_add_files(process.path)
    repo_utils.git_initial_commit(process.path)
    repo_utils.pelican_generate(process.path)
    #repo_utils.github_pages_import(process.path)
    ssh_url = repo_utils.github_create_repo(repo.user.access_token, repo.name)
    key_id = repo_utils.github_add_ssh_key(
        repo.user.access_token, repo.user.username,
        repo.name, public_key
    )
    repo_utils.git_remote_add(process.path, ssh_url)
    repo_utils.git_push_origin(process.path)
    repo_utils.github_remove_ssh_key(
        repo.user.access_token, repo.user.username, repo.name, key_id
    )

    process.stage = 'end'
