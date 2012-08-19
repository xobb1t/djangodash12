import os

from celery.task import task
from django.conf import settings

from repositories import utils as repo_utils
from .utils import (parse_blog_posts, create_pelican_configs,
    create_pelican_instance)


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
    process.stage = 1

    blog = process.blog
    repo = process.repo

    # Create pelican environemnt
    create_pelican_instance(process)
    process.stage = 5
    parse_blog_posts(process, settings.PARSE_PAGES_COUNT)
    process.stage = 35
    create_pelican_configs(process)
    process.stage = 40

    public_key_path = os.path.join(settings.KEYS_ROOT, 'id_rsa.pub')
    with open(public_key_path) as f:
        public_key = f.read()
    repo_utils.git_init_repo(process.path)
    process.stage = 45
    repo_utils.git_add_files(process.path)
    process.stage = 50
    repo_utils.git_initial_commit(process.path)
    process.stage = 55
    repo_utils.pelican_generate(process.path)
    process.stage = 60
    repo_utils.add_cname_in_branches(process.path, repo.cname)
    process.stage = 65
    ssh_url = repo_utils.github_create_repo(repo.user.access_token, repo.name)
    process.stage = 70
    key_id = repo_utils.github_add_ssh_key(
        repo.user.access_token, repo.user.username,
        repo.name, public_key
    )
    process.stage = 75
    repo_utils.git_remote_add(process.path, ssh_url)
    process.stage = 80
    repo_utils.git_push_origin(process.path)
    process.stage = 85
    repo_utils.github_pages_import(process.path)
    process.stage = 95
    repo_utils.github_remove_ssh_key(
        repo.user.access_token, repo.user.username, repo.name, key_id
    )

    process.stage = 100
