from dotenv import load_dotenv
from Quiz_App.settings.development import *

import django_heroku
import os

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [".herokuapps.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

django_heroku.settings(locals())
