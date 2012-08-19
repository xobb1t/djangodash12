import os
import stat
from subprocess import Popen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string


class Command(BaseCommand):

    help = 'makes ssh keys'

    def handle(self, *args, **kwargs):
        keys_dir = settings.KEYS_ROOT
        try:
            os.makedirs(keys_dir)
        except OSError:
            pass
        id_rsa = os.path.join(keys_dir, 'id_rsa')
        if not os.path.exists(id_rsa):
            Popen(
                'ssh-keygen -q -N '' -t rsa -f {0}'.format(id_rsa).split(' ')
            ).wait()
        git_ssh = settings.GIT_SSH
        with open(git_ssh, 'w') as f:
            f.write(render_to_string('git_ssh.sh_tpl', {}))
        os.chmod(git_ssh, stat.S_IXOTH)
