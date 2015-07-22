import os
import dj_database_url


SITE_ID = 10

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {'default': dj_database_url.config()}


NOTIFICATIONS_RECEIVERS = (
    ('John Doe', 'john@doe.com'),
)

# SOCIAL AUTH KEYS (python-social-auth)
SOCIAL_AUTH_FACEBOOK_KEY = '543367435806663'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e3640b667f76f32235d3d95d79a27f87'
SOCIAL_AUTH_TWITTER_KEY = 'dTneRzvBNxy6i5NlvAzXQ3zBM'

# AWS CLOUD
AWS_S3_ACCESS_KEY_ID = 'AKIAJBBUKIWHQ5Q3GEDQ'     # enter your access key id
AWS_S3_SECRET_ACCESS_KEY = 'P+oH5wwk7N0WmWEcCtA1Wj5hZLy0xxNmqyKJ+z4L' # enter your secret access key
AWS_STORAGE_BUCKET_NAME = 'raredoor-prod'
