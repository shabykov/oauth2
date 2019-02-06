from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'weboauth2',
        'USER': 'smith',
        'PASSWORD': 'KuP*pDoA#DwchCTL',
        'HOST': 'postgres',
        'PORT': 5432
    }
}

ALLOWED_HOSTS = ['*']