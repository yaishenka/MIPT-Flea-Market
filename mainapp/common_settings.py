import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open('security_info.json') as json_secret:
    secret_data = json.load(json_secret)
    SECRET_KEY = secret_data['django_secret_key']
    VK_API_KEY = secret_data['vk_api_key']
    SOCIAL_AUTH_VK_OAUTH2_KEY = secret_data['SOCIAL_AUTH_VK_OAUTH2_KEY']
    SOCIAL_AUTH_VK_OAUTH2_SECRET = secret_data['SOCIAL_AUTH_VK_OAUTH2_SECRET']
    POSTGRES_PASSWORD = secret_data['POSTGRES_PASSWORD']

VK_API_VERSION = 5.90

ALLOWED_HOSTS = ['127.0.0.1', '178.62.97.148', 'yaishenka.site', 'localhost']

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.open_id.OpenIdAuth',
    'users.backends.AuthBackend',
]

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/flea_market/'
LOGOUT_REDIRECT_URL = '/flea_market/'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'fleamarket',
    'vk_sender',
    'subscriptions',
    'social_django'
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'mainapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainapp.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = './static/'
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
MEDIA_URL = '/media/'


SOCIAL_AUTH_VK_OAUTH2_SCOPE = []

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'users.pipeline.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'users.pipeline.create_user_by_social',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',


    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social_core.pipeline.user.user_details',
)
