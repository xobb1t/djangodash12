import os
import requests
import simplejson

from django.conf import settings

from pelican import Pelican
from pelican.settings import read_settings

from subprocess import Popen


class RepoError(Exception):
    pass


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


def git_init_repo(files_path):
    if Popen(['git', 'init'], cwd=files_path).wait():
        raise RepoError("Can't create git repository")


def git_add_files(files_path):
    if Popen(['git', 'add', '.'], cwd=files_path).wait():
        raise RepoError("Can't add files in git repository")


def git_initial_commit(files_path):
    if Popen(['git', 'commit', '-m', 'Initial commit'], cwd=files_path).wait():
        raise RepoError("Can't create initial commit")


def github_create_repo(access_token, repo_name):
    post_data_dict = {
        'name': repo_name,
        'description': 'Static Pelican-powered blog'
    }
    response_json = requests.post(
        '{0}/user/repos?access_token={1}'.format(
            settings.GITHUB_API_HOST, access_token
        ),
        data=simplejson.dumps(post_data_dict),
        headers={'Accept': 'application/json'}
    )
    if response_json.status_code != 201:
        raise RepoError("Don't create repo in github")

    response_dict = simplejson.loads(response_json.content)
    return response_dict['ssh_url']


def github_add_ssh_key(access_token, user, repo_name, ssh_key):
    post_data_dict = {
        'title': 'key for push Pelican blog generator',
        'key': ssh_key,
    }
    response_json = requests.post(
        '{0}/repos/{1}/{2}/keys?access_token={3}'.format(
            settings.GITHUB_API_HOST, user, repo_name, access_token
        ),
        data=simplejson.dumps(post_data_dict),
        headers={'Accept': 'application/json'}
    )
    response_dict = simplejson.loads(response_json.text)
    if 'id' not in response_dict:
        raise RepoError("Don't add ssh-key in repo")
    return response_dict['id']


def git_remote_add(files_path, ssh_url):
    cmd = ['git', 'remote', 'add', 'origin', ssh_url]
    if Popen(cmd, cwd=files_path).wait():
        raise RepoError("Can't add git remote!")


def git_push_origin(files_path):
    if Popen(['git', 'push', '-u', 'origin', 'master'], cwd=files_path).wait():
        raise RepoError("Can't push into git remote repo!")


def github_remove_ssh_key(access_token, user, repo_name, key_id):
    response = requests.delete(
        '{0}/repos/{1}/{2}/keys/{3}?access_token={4}'.format(
            settings.GITHUB_API_HOST, user, repo_name, key_id, access_token
        )
    )
    if response.status_code != 204:
        raise RepoError("Can't remove ssh key!")


def pelican_generate(files_path):
    content_path = os.path.join(files_path, 'content')
    conf_path = os.path.join(files_path, 'pelicanconf.py')
    output_path = os.path.join(files_path, 'output')
    settings = read_settings(conf_path)
    pelican = Pelican(
        settings=settings,
        path=content_path,
        output_path=output_path,
        theme='notmyidea'
    )
    pelican.run()


def add_cname_file(files_path, domain):
    cmd = ['echo', domain, '>', 'CNAME']
    if Popen(cmd, cwd=files_path).wait():
        raise RepoError("Can't add cname file in branch!")


def git_change_branch(files_path, branch):
    if Popen(['git', 'checkout', branch], cwd=files_path).wait():
        raise RepoError("Can't change branch to {0}!".format(branch))


def add_cname(files_path, domain):
    if domain is None:
        return
    add_cname_file(files_path, domain)
