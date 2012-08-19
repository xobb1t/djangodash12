import os
from subprocess import Popen

from django.conf import settings
from django.core.management.base import BaseCommand


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
