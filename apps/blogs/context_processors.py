import urllib
from django.conf import settings


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
