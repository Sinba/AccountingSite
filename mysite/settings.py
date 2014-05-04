"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd$in9ia699(b4@^49^o*a!!agjmj)%$))#dh(iwtt-sm_zj63('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'mptt',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/login/'

LOGOUT_URL = '/logout/'

LOGIN_REDIRECT_URL = '/'


ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'mysql.cnf'),
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
DATE_INPUT_FORMATS = (
   '%d %B %Y',
   '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
   '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
   '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
   '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
   '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
)

DATE_FORMAT = 'j N Y'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False 

USE_L10N = False 

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
