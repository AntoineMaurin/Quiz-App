import os

from quiz_app.settings.development import *

SECRET_KEY = os.environ.get(
    'SECRET_KEY', '8fsm7s-poju5ht*%j$@__r8(orf%o=nvei1l9q#0v$^1w+pu8=')

DEBUG = False

ALLOWED_HOSTS = [".herokuapps.com"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Quiz_DB',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
