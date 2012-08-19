import urllib

from django.conf import settings
from django.utils.functional import SimpleLazyObject

from project.core.utils import get_object_or_None

from .models import User, Repo


def github(request):

    def get_user():
        user_id = request.session.get('repo_user_id')
        return get_object_or_None(User, pk=user_id)

    def get_repo():
        repo_id = request.session.get('repo_id')
        return get_object_or_None(Repo, pk=repo_id)

    def get_auth_url():
        query_params = {
            'response_type': 'token',
            'client_id': settings.GITHUB_ID,
            'redirect_uri': settings.GITHUB_CALLBACK_URL,
            'scope': ','.join(settings.GITHUB_SCOPES)
        }
        query_string = urllib.urlencode(query_params)
        auth_url = '{0}?{1}'.format(settings.GITHUB_AUTH_URL, query_string)
        return auth_url

    return {
        'github_user': SimpleLazyObject(get_user),
        'github_repo': SimpleLazyObject(get_repo),
        'github_auth_url': SimpleLazyObject(get_auth_url)
    }
