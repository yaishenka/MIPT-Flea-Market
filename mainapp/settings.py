from .common_settings import *

DEBUG = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None
USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}