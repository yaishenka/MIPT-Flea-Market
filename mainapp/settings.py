from .common_settings import *

DEBUG = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None
USE_X_FORWARDED_HOST = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}