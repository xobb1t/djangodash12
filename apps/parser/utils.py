import slumber
import requests

from django.template.loader import render_to_string


def get_slumber_api(root, access_token):
    session = requests.session(
        params={'access_token': access_token}
    )
    return slumber.API(root, session=session)


def parse_blog_posts(process, max_pages, page_token=None, page_size=20):
    api = get_slumber_api(
        settings.BLOGGER_API_ROOT,
        process.blog.source.access_token
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
