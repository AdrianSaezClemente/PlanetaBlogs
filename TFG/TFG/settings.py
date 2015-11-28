"""
Django settings for TFG project.

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
SECRET_KEY = '+2#5&97_k1$8j4nwf47oo#b*8=t2nynb5b!5_va#^4og+6%yny'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 


TEMPLATE_DEBUG = True

USE_TZ = True

TIME_ZONE = 'Europe/Madrid'

ALLOWED_HOSTS = []

TEMPLATE_DIRS = ['/home/asaez/FinalTFG/PlanetaBlogs/TFG/plantillas']

# Application definition

# Redirect when login is correct.
LOGIN_REDIRECT_URL = "/planetablogs"
# Redirect when login is not correct.
LOGIN_URL = '/planetablogs/login'


GRAPH_MODELS = {
	'all_applications':True,
	'group_models':True,
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'planetablogs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TFG.urls'

WSGI_APPLICATION = 'TFG.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.sqlite3',
	'NAME': 'bbdd.sqlite',	#Poner el nombre vale
	'USER': '', #Para BBDD que no sea SQLite
	'PASSWORD': '', #Para BBDD que no sea SQLite
	'HOST': '', #Para BBDD que no sea SQLite
	'PORT': '', #Para BBDD que no sea SQLite
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

SETTINGS_PATH = '/home/asaez/FinalTFG/PlanetaBlogs/TFG'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join('/home/asaez/FinalTFG/PlanetaBlogs/TFG/', "static"),
)

MEDIA_ROOT = os.path.join('/home/asaez/FinalTFG/PlanetaBlogs/TFG/static/imagenes')

