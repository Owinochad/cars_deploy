"""
Django settings for cars_competition project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import Config, RepositoryEnv
import paypalrestsdk


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.prod')
  # Correct path to .env.dev

if not os.path.exists(env_file_path):
    raise FileNotFoundError(f"{env_file_path} not found.")

# Initialize the config with the correct path
config = Config(RepositoryEnv(env_file_path))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')
PAYPAL_API_URL = config('PAYPAL_API_URL')

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_CLIENT_SECRET,
})

CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
BUSINESS_SHORT_CODE = config('BUSINESS_SHORT_CODE')
PASSKEY = config('PASSKEY')
DPO_COMPANY_TOKEN = config('DPO_COMPANY_TOKEN')
DPO_BASE_URL = config('DPO_BASE_URL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS= []
# CSRF_TRUSTED_ORIGINS=[
#     'http://127.0.0.1:8000',
#     ]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_REQUIRED = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'competition.apps.CompetitionConfig',
    'mpesa_payments',
    'rest_framework',

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.twitter_oauth2',
    # 'allauth.socialaccount.providers.telegram',
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    'user.apps.UserConfig',
    'crispy_forms',
    'crispy_bootstrap4',

    # 'paypal.standard.ipn',
    'corsheaders',

]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'


CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    #coreheaders
    "corsheaders.middleware.CorsMiddleware",

    #other middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "allauth.account.middleware.AccountMiddleware",
]

# Environment Variables
SECRET_KEY = config('SECRET_KEY')


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

    # 'twitter': {
    #     'APP': {
    #         'client_id': config('SOCIAL_AUTH_TWITTER_CLIENT_ID'),
    #         'secret': config('SOCIAL_AUTH_TWITTER_SECRET'), 
    #         'key': ''
    #     }
    # },
}


ROOT_URLCONF = 'cars_competition.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cars_competition.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR, 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'

PAYPAL_RECEIVER_EMAIL = 'bizrowino899@gmail.com'
PAYPAL_TEST = True


