import os
from .base import *
from decouple import Config, RepositoryEnv

# Load environment variables from .env.dev file
env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env.dev')
  # Correct path to .env.dev

if not os.path.exists(env_file_path):
    raise FileNotFoundError(f"{env_file_path} not found.")

# Initialize the config with the correct path
config = Config(RepositoryEnv(env_file_path))

WSGI_APPLICATION = 'cars_competition.wsgi_dev.application'


# Environment Variables
SECRET_KEY = config('SECRET_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_CLIENT_ID'),
            'secret': config('SOCIAL_AUTH_GITHUB_SECRET'), 
            'key': ''
        }
    },

    'google': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
            'secret': config('SOCIAL_AUTH_GOOGLE_SECRET'), 
            'key': ''
        }
    },
}

DEBUG = True

ALLOWED_HOSTS = []

# Development database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static and Media Files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
