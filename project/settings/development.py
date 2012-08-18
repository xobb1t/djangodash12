import os
from .common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'sqlite3.db'),
    }
}

for i, middleware in enumerate(MIDDLEWARE_CLASSES):
    if 'CommonMiddleware' in middleware:
        mcs = list(MIDDLEWARE_CLASSES)
        mcs.insert(i + 1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        MIDDLEWARE_CLASSES = tuple(mcs)
        INSTALLED_APPS += ('debug_toolbar',)
        break

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('127.0.0.1',)
