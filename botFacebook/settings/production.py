import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

#mongodb+srv://petvillano:123@cluster.abnui.mongodb.net/pet?retryWrites=true&w=majority	
#"host": 'mongodb+srv://petvillano:123@cluster.abnui.mongodb.net/test',

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        "CLIENT": {
           "name": 'pet',	       
	       "host": os.environ.get('MONGODB_URI'),
           "username": 'petvillano',
           "password": '123',
           "authMechanism": "SCRAM-SHA-1",
        }, 
    }
}

STATICFILES_DIRS = (BASE_DIR, 'static')