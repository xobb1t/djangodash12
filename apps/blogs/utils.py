import requests
import simplejson as json

from django.conf import settings


class AuthError(Exception):
    pass


def get_tokens(code):
    data = {
        'code': code,
        'client_id': settings.GOOGLE_ID,
        'client_secret': settings.GOOGLE_SECRET,
        'redirect_uri': settings.GOOGLE_CALLBACK_URL,
        'grant_type': 'authorization_code',
    }
    r = requests.post(settings.GOOGLE_TOKEN_URL, data=data)
    if r.status_code == 200:
        data = json.loads(r.content)
        if not data.get('error'):
            return data
    raise AuthError


def blogger_resource(resource, access_token):
    url = '{0}{1}?access_token={2}'.format(
        settings.BLOGGER_API_ROOT, resource, access_token
    )
    print url
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        if not data.get('error'):
            return data
    return {}
