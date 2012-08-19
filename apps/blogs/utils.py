import requests
import slumber
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


def api_resource(root, resource, access_token):
    url = '{0}{1}?access_token={2}'.format(
        root, resource, access_token
    )
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        if not data.get('error'):
            return data
    return {}


def get_slumber_api(root, access_token):
    session = requests.session(
        params={'access_token': access_token}
    )
    return slumber.API(root, session=session)


def get_blogpost_count(blog):
    api = get_slumber_api(
        settings.BLOGGER_API_ROOT,
        blog.source.access_token
    )
    data = api.blogs(blog.identificator).get()
    return data.get('posts', {}).get('totalItems', 0)


def get_blog_posts(blog, max_pages, page_token=None, page_size=20):
    api = get_slumber_api(
        settings.BLOGGER_API_ROOT,
        blog.source.access_token
    )
    data = api.blogs(blog.identificator).posts().get(
        pageToken=page_token, maxResults=page_size,
    )
    nextPageToken = data.get('nextPageToken')

    result = data.get('items', [])
    max_pages -= 1
    if not max_pages <= 0 and nextPageToken is not None:
        result.extend(get_blog_posts(blog, nextPageToken))
    return result
