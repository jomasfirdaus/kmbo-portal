from .base import *
from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Database Configuration for Development
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {'unix_socket': '/tmp/mysql.sock',},
        'TIME_ZONE': 'Asia/Tokyo',
    },
}


# Minio Configuration for Development
MINIO_END_POINT = config('MINIO_END_POINT')
MINIO_BUCKET_NAME = config('MINIO_BUCKET_NAME')
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY')
MINIO_REGION = config('MINIO_REGION')
MINIO_USE_HTTPS = True