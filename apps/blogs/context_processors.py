import urllib

from django.conf import settings
from django.utils.functional import SimpleLazyObject


def google_auth_url(request):
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
    return {'google_auth_url': auth_url}


def blog_source(request):
    def get_blog_source():
        return request.session.get('blog_source', None)
    return {'blog_source': SimpleLazyObject(get_blog_source)}
