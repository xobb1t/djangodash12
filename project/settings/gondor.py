import os
import redis
import urlparse

from random import choice

from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

SITE_ID = 1  # set this to match your Sites setup

DATA_DIR = os.environ["GONDOR_DATA_DIR"]

MEDIA_ROOT = os.path.join(DATA_DIR, "site_media", "media")
STATIC_ROOT = os.path.join(DATA_DIR, "site_media", "static")

SECRET_KEY_FILE = os.path.join(DATA_DIR, 'secret.txt')
if not os.path.exists(SECRET_KEY_FILE):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = ''.join(choice(chars) for i in range(50))
    with open(SECRET_KEY_FILE, 'w') as f:
        f.write(SECRET_KEY)
else:
    with open(SECRET_KEY_FILE) as f:
        SECRET_KEY = f.read()

MEDIA_URL = "/site_media/media/"
STATIC_URL = "/site_media/static/"
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

FILE_UPLOAD_PERMISSIONS = 0640

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "propagate": True,
        },
    }
}

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])

    conn = redis.Redis(
        host=url.hostname,
        port=url.port,
        password=url.password
    )

    BROKER_TRANSPORT = "redis"
    BROKER_HOST = url.hostname
    BROKER_PORT = url.port
    BROKER_VHOST = "0"
    BROKER_PASSWORD = url.password

    CELERY_RESULT_BACKEND = "redis"
    CELERY_REDIS_HOST = url.hostname
    CELERY_REDIS_PORT = url.port
    CELERY_REDIS_PASSWORD = url.password


BLOGS_ROOT = os.path.join(DATA_DIR, 'blogs')
KEYS_ROOT = os.path.join(DATA_DIR, 'keys')
os.environ.setdefault('KEYS_ROOT', KEYS_ROOT)

scripts_dir = os.path.join(PACKAGE_ROOT, 'scripts')
os.environ.setdefault('GIT_SSH_DIR', scripts_dir)
os.environ.setdefault('GIT_SSH', os.path.join(scripts_dir, 'git_ssh.sh'))
