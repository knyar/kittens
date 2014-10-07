import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = { 'default': { } }

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = ('kittens')

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../files')
MEDIA_URL = '/kittens/files'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../templates'))

# set this in local_settings.py
#FLICKR_API_KEY = ''

from local_settings import *
