import os
import re
import requests
import slumber
from StringIO import StringIO
from subprocess import Popen

from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string

from html2text import html2text as html2text_orig


link_re = re.compile(r"https?://([^ \n]+\n)+[^ \n]+", re.MULTILINE)


def html2text(html):
    """use html2text but repair newlines cutting urls"""
    txt = html2text_orig(html)
    links = list(link_re.finditer(txt))
    # replace links
    out = StringIO()
    pos = 0
    for l in links:
        out.write(txt[pos:l.start()])
        out.write(l.group().replace("\n", ""))
        pos = l.end()
    out.write(txt[pos:])
    return out.getvalue()


def get_api(root, access_token):
    session = requests.session(
        params={'access_token': access_token}
    )
    return slumber.API(root, session=session)


def parse_blog_posts(process, max_pages, page_token=None, page_size=20):
    blog = process.blog
    api = get_api(
        settings.BLOGGER_API_ROOT,
        blog.source.access_token
    )
    data = api.blogs(blog.identificator).posts().get(
        pageToken=page_token, maxResults=page_size,
    )
    nextPageToken = data.get('nextPageToken')
    posts = data.get('items', [])
    if not posts:
        return
    convert_blog_posts(process, posts)

    max_pages -= 1
    if not max_pages <= 0 and nextPageToken is not None:
        parse_blog_posts(process, max_pages, nextPageToken, page_size)


def get_post_slug(domain, full_url):
    slug = full_url.replace('http://{0}'.format(domain), '')
    slug = slug.replace('.html', '')
    return slug[1:]


def create_pelican_instance(process):
    content_root = os.path.join(process.path, 'content')
    try:
        os.makedirs(content_root)
    except OSError:
        pass
    pelican_src = os.path.join(settings.PACKAGE_ROOT, 'pelican')
    Popen(['cp', '-r', '.', process.path], cwd=pelican_src).wait()


def convert_blog_posts(process, posts):
    content_root = os.path.join(process.path, 'content')
    domain = process.blog.domain
    for post in posts:
        slug = get_post_slug(domain, post.get('url'))
        file_name = slug.replace('/', '-')
        file_path = os.path.join(content_root, file_name)
        file_path = '{0}.md'.format(file_path)
        convert_blog_post(post, slug, file_path)


def convert_post_content(post):
    content = post.get('content', '')
    return html2text(content)


def convert_blog_post(post, slug, file_path):
    published = post.get('published', '')
    date_string = published[:-6]
    date_format = '%Y-%m-%dT%H:%M:%S'
    result = render_to_string('parser/post.md_tpl', {
        'date': datetime.strptime(date_string, date_format),
        'post': post,
        'slug': slug,
        'content': convert_post_content(post),
    })
    with open(file_path, 'w') as f:
        f.write(result.encode('utf-8'))


def create_pelican_configs(process):
    blog = process.blog
    repo = process.repo
    if repo.cname:
        site_url = repo.cname
    else:
        site_url = '{0}.github.com/{1}'.format(repo.user.username, repo.name)
    result = render_to_string('parser/pelicanconf.py_tpl', {
        'blog': blog, 'repo': repo, 'site_url': site_url
    })
    file_path = os.path.join(process.path, 'pelicanconf.py')
    with open(file_path, 'w') as f:
        f.write(result.encode('utf-8'))

    result = render_to_string('parser/publishconf.py_tpl', {
        'blog': blog, 'repo': repo, 'site_url': site_url,
    })
    file_path = os.path.join(process.path, 'publishconf.py')
    with open(file_path, 'w') as f:
        f.write(result.encode('utf-8'))
