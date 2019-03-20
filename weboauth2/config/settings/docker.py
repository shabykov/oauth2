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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'username'
EMAIL_HOST_PASSWORD = 'P@ssw0rd'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'IT Team <noreply@authservice.com>'