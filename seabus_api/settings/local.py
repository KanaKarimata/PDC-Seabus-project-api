from .base import *
import os
import environ

env = environ.Env()
env_file = '.env.local'
environ.Env.read_env(env_file)

print(f"Database settings: {DATABASES['default']}")

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
  "http://localhost:8080",
  "http://localhost:8081",
]

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': env('DATABASE_NAME'),
    'USER': env('DATABASE_USER'),
    'PASSWORD': env('DATABASE_PASSWORD'),
    'HOST': env('DATABASE_HOST'),
    'PORT': env('DATABASE_PORT'),
    'OPTIONS': {
        'options': env('DATABASE_OPTIONS', default='-c search_path=seabus')
    }
}