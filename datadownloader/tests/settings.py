# -*- coding: utf-8 -*-

import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SECRET_KEY = 'abcde123'

DATA_DOWNLOADER_PATH = os.path.join(BASE_DIR, 'datas')
MEDIA_ROOT = os.path.join(BASE_DIR, 'medias')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
        ]
    },
]

INSTALLED_APPS = [
    'datadownloader',
]

SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_ROOT = '/srv/www/'
SENDFILE_URL = '/protected'
