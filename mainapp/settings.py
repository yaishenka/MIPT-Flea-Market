from .common_settings import *

DEBUG = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None
USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres_db',
        'USER' : 'flea_market',
        'PASSWORD' : POSTGRES_PASSWORD,
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}
