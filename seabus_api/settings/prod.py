from .base import *
import os
import environ

env = environ.Env()
env_file = '.env.prod'
environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['api.candidree.com', 'candidree.com', 'www.candidree.com']

CORS_ALLOWED_ORIGINS = [
  "https://candidree.com",
  "https://www.candidree.com",
]

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': env('DATABASE_NAME'),
    'USER': env('DATABASE_USER'),
    'PASSWORD': env('DATABASE_PASSWORD'),
    'HOST': env('DATABASE_HOST'),
    'PORT': env('DATABASE_PORT')
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]