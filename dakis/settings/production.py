# pylint: disable=wildcard-import,unused-wildcard-import

from dakis.settings.base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['dakis.lt', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dakis',
        'USER': 'dakis',
    }
}

LOGGING['root'] = {
    'level': 'WARNING',
    'handlers': ['stdout'],
}

SOCIALACCOUNT_PROVIDERS['persona']['AUDIENCE'] = 'dakis.lt'
