from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r1ip(ha6tt3*s6xkd#qnq=3wgx+t31+f@t5a19ygh&ng72!qq2'

DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ["demo-kmbo.tualiqui.com", "kmbo.tl", "www.kmbo.tl"]

CSRF_TRUSTED_ORIGINS = [
    'https://demo-kmbo.tualiqui.com',
    'http://demo-kmbo.tualiqui.com',
    'https://kmbo.tl',
    'http://kmbo.tl',
    'https://www.kmbo.tl',
    'http://www.kmbo.tl',
]

# ------------------ APPS ------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # external apps
    'crispy_forms',
    'crispy_bootstrap4',
    'ckeditor',
    'embed_video',
    'tinymce',

    # internal apps
    'main',
    'portal',
]

# ------------------ MIDDLEWARE ------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # IMP: locale middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'kmbo.urls'

# ------------------ TEMPLATES ------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kmbo.wsgi.application'

# ------------------ DATABASE ------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'db_kmbo_dev',
#     'USER': 'db_kmbo_dev',
#     'PASSWORD': 'tEroc=op7#zi',
#     'HOST': 'localhost',
#     'PORT': "3306",
#     'OPTIONS': {
#         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#     }
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kmbo_db_demo',
        'USER': 'kmbo_db_demo',
        'PASSWORD': '80ldY6LwiB9QsUqV',
        'HOST': 'srv-captain--mysql-8-db',
        'PORT': "3306",
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# ------------------ PASSWORD VALIDATION ------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------ I18N + Locale ------------------

from django.conf.locale import LANG_INFO

# Adisiona Tetun manuál
LANG_INFO.update({
    'tet': {
        'bidi': False,
        'code': 'tet',
        'name': 'Tetun',
        'name_local': 'Tetun',
    }
})

LANGUAGE_CODE = 'tet'  # Default: Tetun

LANGUAGES = [
    ('tet', 'Tetun'),
    ('pt', 'Português'),
    ('en', 'English'),
]

TIME_ZONE = 'Asia/Dili'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# ------------------ STATIC + MEDIA ------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------ CKEDITOR ------------------
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': 'auto',
        'extraPlugins': ','.join(['codesnippet']),
    },
}

# ------------------ CRISPY FORMS ------------------
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap4',)

# ------------------ DEFAULT PK FIELD ------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/Users/macos/Desktop/kmbowebsite/kmbo/log.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

