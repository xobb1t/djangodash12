import urllib

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from project.core.utils import get_object_or_None

from .models import Blog, Source


def blogger(request):

    def get_auth_url():
        data = {
            'response_type': 'code',
            'client_id': settings.GOOGLE_ID,
            'redirect_uri': settings.GOOGLE_CALLBACK_URL,
            'scope': ' '.join(settings.GOOGLE_SCOPES),
            'state': request.path,
            'access_type': 'online'
        }
        query_string = urllib.urlencode(data)
        auth_url = '{0}?{1}'.format(settings.GOOGLE_AUTH_URL, query_string)
        return auth_url

    def get_blog_source():
        blog_source_id = request.session.get('blog_source_id')
        return get_object_or_None(Source, pk=blog_source_id)

    def get_blog():
        blog_id = request.session.get('blog_id')
        return get_object_or_None(Blog, pk=blog_id)

    return {
        'blog_source': SimpleLazyObject(get_blog_source),
        'blog': SimpleLazyObject(get_blog),
        'google_auth_url': SimpleLazyObject(get_auth_url),
    }
