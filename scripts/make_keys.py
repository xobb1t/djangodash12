#!/usr/bin/env python

import os
from subprocess import Popen

def main():
    root = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
    keys_dir = os.path.join(root, 'keys')
    try:
        os.makedirs(keys_dir)
    except OSError:
        pass
    id_rsa = os.path.join(keys_dir, 'id_rsa')
    if not os.path.exists(id_rsa):
        Popen(
            'ssh-keygen -q -N '' -t rsa -f {0}'.format(id_rsa).split(' ')
        ).wait()


if __name__ == '__main__':
    main()
