# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '^%7!u-&ewhioc&g6zw-jfc#tdu(v4khmif%&e4aa^6p4dj_a0g'
DEBUG = True
ALLOWED_HOSTS = ['x-coursee.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'material',
    'material.frontend',
    'material.admin',

    'x_coursee',
    'zite',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'x_coursee.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'x_coursee.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'xcs',
        'USER': 'xcs',
    },
    'default11': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xcsbot',
        'USER': 'xcsbot',
        'PASSWORD': 'Ua3Hezai',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'read_default_file': '/etc/my.cnf',
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
        }
    },
    "commands": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "TIMEOUT": 3600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
        }
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/xcs/static/'
STATIC_ROOT = '/srv/x-coursee.com/xcs_static'

MEDIA_URL = '/xcs/media/'
MEDIA_ROOT = '/srv/x-coursee.com/xcs_media'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s:  %(pathname)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'syslog': {
            'format': '%(pathname)s %(message)s',
        },
    },
    'handlers': {
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'user',
            'address': ('localhost', 514),
            'formatter': 'syslog'
        },
        'systemd-journald': {
            'level': 'DEBUG',
            'class': 'systemd.journal.JournalHandler',
            'formatter': 'syslog'
        },
    },
    'loggers': {
        'default': {
            'handlers': ['systemd-journald'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

TELEGRAM_BOT = {
    'name': 'NotifierTestBot',  # used in url-links like http://t.me/my_cool_bot?start
    'token': '329702714:AAHN90R9XV-nvxa_rNSIJQTxpE2MBOeKQlQ',
    'webhook_url': 'https://x-coursee.com/xcs/tgbotwebhook/',
}
