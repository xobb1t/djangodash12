import requests
import simplejson

from django.conf import settings


def get_access_data(code):
    post_data_dict = {
        'client_id': settings.GITHUB_ID,
        'redirect_uri': settings.GITHUB_CALLBACK_URL,
        'client_secret': settings.GITHUB_SECRET,
        'code': code
    }
    response_json = requests.post(
        settings.GITHUB_ACCESS_TOKEN_URL,
        data=post_data_dict,
        headers={'Accept': 'application/json'}
    )
    return simplejson.loads(response_json.text)


def get_user_info(access_token):
    response_json = requests.get(
        '{0}/user?access_token={1}'.format(
            settings.GITHUB_API_HOST, access_token
        )
    )
    response_dict = simplejson.loads(response_json.text)
    return (response_dict.get('id', None), response_dict.get('login', None))


def repo_exists(access_token, user, repo):
    response = requests.get(
        '{0}/repos/{1}/{2}?access_token={3}'.format(
            settings.GITHUB_API_HOST, user, repo, access_token
        )
    )
    return response.status_code != 404
