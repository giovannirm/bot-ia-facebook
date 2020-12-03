from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        "CLIENT": {
           "name": 'pet',
           "host": 'mongodb+srv://petvillano:123@cluster.abnui.mongodb.net/test',
           "username": 'petvillano',
           "password": '123',
           "authMechanism": "SCRAM-SHA-1",
        }, 
    }
}

STATICFILES_DIRS = (BASE_DIR, 'static')