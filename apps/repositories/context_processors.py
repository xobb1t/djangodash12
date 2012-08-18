import urllib

from django.conf import settings
from django.utils.functional import SimpleLazyObject


def github_auth_url(request):
    query_params = {
        'response_type': 'token',
        'client_id': settings.GITHUB_ID,
        'redirect_uri': settings.GITHUB_CALLBACK_URL,
        'scope': ','.join(settings.GITHUB_SCOPES)
    }
    query_string = urllib.urlencode(query_params)
    auth_url = '{0}?{1}'.format(settings.GITHUB_AUTH_URL, query_string)
    return {'github_auth_url': auth_url}


def github_user(request):
    def get_github_user():
        return request.session.get('repo_user', None)
    return {'github_user': SimpleLazyObject(get_github_user)}
