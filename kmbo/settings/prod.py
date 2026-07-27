import os
from .base import *
from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS').split(',')

# Deployed behind a reverse proxy (Caprover/nginx) that terminates TLS and
# forwards over plain HTTP, so Django needs to be told which header carries
# the original scheme - otherwise request.is_secure() is always False and
# SECURE_SSL_REDIRECT below would loop forever.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Toggle via env var rather than hardcoding True, so ops can disable it
# without a code change if a given deployment's proxy isn't TLS-terminated.
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

X_FRAME_OPTIONS = 'DENY'


# MySQL Configuration for Production
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'TIME_ZONE': 'UTC',
    },
}


# Minio Configuration for Production
MINIO_END_POINT = config('MINIO_END_POINT')
MINIO_BUCKET_NAME = config('MINIO_BUCKET_NAME')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')
MINIO_REGION = config('MINIO_REGION')
MINIO_USE_HTTPS = True