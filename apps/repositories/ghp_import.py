#! /usr/bin/env python
#
# This file is part of the ghp-import package released under
# the Tumbolia Public License. See the LICENSE file for more
# information.
# Copy package from https://github.com/davisp/ghp-import
# Because unable to import this

import optparse as op
import os
import subprocess as sp
import signal
import sys
import time


__usage__ = "%prog [OPTIONS] DIRECTORY"


def subprocess_setup():
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)


def _enc(text):
    if not isinstance(text, bytes):
        text = text.encode()
    return text


if sys.version_info >= (2, 6, 0):
    enc = _enc
else:
    enc = lambda t: t


def is_repo(d):
    if not os.path.isdir(d):
        return False
    if not os.path.isdir(os.path.join(d, 'objects')):
        return False
    if not os.path.isdir(os.path.join(d, 'refs')):
        return False

    headref = os.path.join(d, 'HEAD')
    if os.path.isfile(headref):
        return True
    if os.path.islink(headref) and os.readlink(headref).startswith("refs"):
        return True
    return False


def find_repo(path):
    if is_repo(path):
        return True
    if is_repo(os.path.join(path, '.git')):
        return True
    (parent, ignore) = os.path.split(path)
    if parent == path:
        return False
    return find_repo(parent)


def try_rebase(remote):
    cmd = ['git', 'rev-list', '--max-count=1', 'origin/gh-pages']
    p = sp.Popen(cmd, preexec_fn=subprocess_setup)
    (rev, ignore) = p.communicate()
    if p.wait() != 0:
        return True
    cmd = ['git', 'update-ref', 'refs/heads/gh-pages', rev.strip()]
    if sp.call(cmd) != 0:
        return False
    return True


def get_config(key):
    p = sp.Popen(['git', 'config', key], preexec_fn=subprocess_setup)
    (value, stderr) = p.communicate()
    return value.strip()


def get_prev_commit():
    cmd = ['git', 'rev-list', '--max-count=1', 'gh-pages']
    p = sp.Popen(cmd, preexec_fn=subprocess_setup)
    (rev, ignore) = p.communicate()
    if p.wait() != 0:
        return None
    return rev.strip()


def mk_when(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    currtz = "%+05d" % (time.timezone / 36) # / 3600 * 100
    return "%s %s" % (timestamp, currtz)


def start_commit(pipe, message):
    uname = get_config("user.name")
    email = get_config("user.email")


def add_file(pipe, srcpath, tgtpath):
    pass


def run_import(srcdir, message):
    cmd = ['git', 'fast-import', '--date-format=raw', '--quiet']
    pipe = sp.Popen(cmd, preexec_fn=subprocess_setup)
    start_commit(pipe, message)
    for path, dnames, fnames in os.walk(srcdir):
        for fn in fnames:
            fpath = os.path.join(path, fn)
            add_file(pipe, fpath, os.path.relpath(fpath, start=srcdir))
    if pipe.wait() != 0:
        sys.stdout.write(enc("Failed to process commit.\n"))


def options():
    return [
        op.make_option('-m', dest='mesg', default='Update documentation',
            help='The commit message to use on the gh-pages branch.'),
        op.make_option('-p', dest='push', default=False, action='store_true',
            help='Push the branch to origin/gh-pages after committing.'),
        op.make_option('-r', dest='remote', default='origin',
            help='The name of the remote to push to. [%default]')
    ]


def main():
    parser = op.OptionParser(usage=__usage__, option_list=options())
    opts, args = parser.parse_args()

    if len(args) == 0:
        parser.error("No import directory specified.")

    if len(args) > 1:
        parser.error("Unknown arguments specified: %s" % ', '.join(args[1:]))

    if not os.path.isdir(args[0]):
        parser.error("Not a directory: %s" % args[0])

    if not find_repo(os.getcwd()):
        parser.error("No Git repository found.")

    if not try_rebase(opts.remote):
        parser.error("Failed to rebase gh-pages branch.")

    run_import(args[0], opts.mesg)

    if opts.push:
        sp.check_call(['git', 'push', opts.remote, 'gh-pages'])


if __name__ == '__main__':
    main()
