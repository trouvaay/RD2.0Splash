import os

from base_social import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 9

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    #'debug_toolbar',
    'django.contrib.sites',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_extensions', # TEMP # to visualize models only
    'easy_thumbnails', # should be declared explicitly
    'storages',
    'rest_framework', # api
    'bootstrap3',
    'localflavor',
    'social.apps.django_app.default',
    'userena',
    'guardian', # for userena

    'raredoor',
    'landing',

    'user',
    'merchant',
    'product',
    'order',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'landing.middleware.RefererMiddleware', # TODO: temp. to collect referers for subscribers
)

ROOT_URLCONF = 'raredoor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.core.context_processors.static',
                'django.core.context_processors.csrf',

                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'raredoor.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# SOCIAL AUTH
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    #'guardian.backends.ObjectPermissionBackend',

    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',

    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'
#SOCIAL_AUTH_LOGIN_ERROR_URL = '/500'
#SOCIAL_AUTH_LOGIN_URL = ''

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    #'social.pipeline.mail.mail_validation',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)


DEFAULT_FROM_EMAIL = 'info@raredoor.com'
SEND_GRID_LOGIN = os.environ.get('SENDGRID_USERNAME', 'default')
SEND_GRID_PASSWORD = os.environ.get('SENDGRID_PASSWORD', 'default')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = SEND_GRID_LOGIN
EMAIL_HOST_PASSWORD = SEND_GRID_PASSWORD


# STORAGE
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = False # use http instead of https
AWS_QUERYSTRING_AUTH = False # don't add complex authentication-related query parameters for requests


# USERENA
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'user.Profile' # almost depricated
USERENA_ACTIVATION_DAYS = 7 # One-week activation window;
USERENA_FORBIDDEN_USERNAMES = (
    'login', 'logout', 'register', 'signup', 'signout',
    'signin', 'activate', 'me', 'password',
)
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True
USERENA_MUGSHOT_GRAVATAR = False
USERENA_MUGSHOT_DEFAULT = '/static/img/avatar.png'
#USERENA_MUGSHOT_SIZE = 100
#USERENA_MUGSHOT_PATH = 'mugshots'

#LOGIN_REDIRECT_URL = reverse_lazy('xxx') # not used by userena
LOGIN_URL = "/accounts/signin/"
LOGOUT_URL = "/accounts/signout/"


""" RESERVED
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('api.renderers.JsonApi','rest_framework.renderers.BrowsableAPIRenderer'),
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'EXCEPTION_HANDLER': 'api.utils.api_exception_handler',
}
"""

#BOOTSTRAP3
BOOTSTRAP3 = {
    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horiozntal forms
    'horizontal_field_class': 'col-md-6',
}


# TEMP TEMP TEMP
SHELF_LIFE = 0


try:
    if os.getenv('PLATFORM') == 'heroku-dev':
        from .heroku_dev import *
    elif os.getenv('PLATFORM') == 'heroku-prod':
        from .heroku_prod import *
    else:
        from .local import *

except ImportError as e:
    print 'Error:', e

