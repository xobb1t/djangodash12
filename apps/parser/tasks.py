from celery.task import task
from django.conf import settings

from .utils import parse_blog_posts, create_pelikan_configs


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
    parse_blog_posts(process, settings.PARSE_PAGES_COUNT)
    create_pelikan_configs(process)
    process.stage = 'end'
