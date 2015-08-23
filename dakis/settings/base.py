import exportrecipe
import pathlib

from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = pathlib.Path(__file__).parents[2]

config = exportrecipe.load(str(PROJECT_DIR / 'settings.json'))


# Django base settings
# https://docs.djangoproject.com/en/stable/ref/settings/

DEBUG = False
ROOT_URLCONF = 'dakis.website.urls'
SECRET_KEY = config.secret_key
MEDIA_URL = '/media/'
MEDIA_ROOT = str(PROJECT_DIR / 'var/www/media')
STATIC_URL = '/static/'
STATIC_ROOT = str(PROJECT_DIR / 'var/www/static')
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('lt', _('Lithuanian')),
    ('en', _('English')),
)
LOCALE_PATHS = (
    str(PROJECT_DIR / 'dakis/locale'),
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        }
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dakis',
    }
}

MIGRATION_MODULES = {
    'account': 'dakis.website.migrations.account',
    'website': 'dakis.website.migrations.website',
    'openid': 'dakis.website.migrations.openid',
    'socialaccount': 'dakis.website.migrations.socialaccount',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'stdout': {
            'format': (
                '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            ),
        },
        'console': {
            'format': '%(levelname)s %(module)s %(message)s',
        },
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'stdout',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django': {
            'propagate': True,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    }
}


# Static assets, see config/assets.cfg
# https://pypi.python.org/pypi/hexagonit.recipe.download

STATICFILES_DIRS = (
    str(PROJECT_DIR / 'parts/jquery'),
    str(PROJECT_DIR / 'parts/bootstrap'),
    str(PROJECT_DIR / 'parts/requirejs'),
)


# django-ompressor settings
# https://pypi.python.org/pypi/django_compressor

INSTALLED_APPS += ('compressor',)
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# django-debug-toolbar settings
# https://django-debug-toolbar.readthedocs.org/

INSTALLED_APPS += (
    'debug_toolbar',
)


# django-extensions
# http://django-extensions.readthedocs.org/

INSTALLED_APPS += (
    'django_extensions',
)


# djangorestframework
# http://www.django-rest-framework.org/
# https://github.com/tomchristie/django-rest-framework
INSTALLED_APPS += (
    'rest_framework',
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}


# django-nose
# https://pypi.python.org/pypi/django-nose

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INSTALLED_APPS += (
    'django_nose',
)


# App settings

SERVER_PROTOCOL = 'http://'
SERVER_NAME = 'dakis.lt'

SERVER_ALIASES = (
    'dakis.lt',
    'www.dakis.lt',
    'localhost',
    '127.0.0.1',
)

INSTALLED_APPS += (
    'dakis.core',
    'dakis.api',
    'dakis.website',
)


SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS += [
    'django.template.context_processors.request',
]

INSTALLED_APPS += (
    'django.contrib.sites',
)
