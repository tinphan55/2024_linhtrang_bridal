"""
Django settings for admin project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from .jazzmin import *
from datetime import timedelta
from datetime import datetime as dt
from dotenv import load_dotenv

# Load environment variables from file
load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+nlr26ab3&*j8fg=q8hr&k0nkl=12s7=cb%g3ur34&o!k7i@lj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CSRF_TRUSTED_ORIGINS = ['https://linhtrangbridal.shop']



ALLOWED_HOSTS = ['*'] 


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clients', 
    'members',
    'services_admin',
    'order',
    'import_export',
    'event_calendar.apps.CalConfig', 
    'frontend',
    'bills', 
    'report',
    # 'iwedding',
    'dbbackup',
    'django_crontab',
    
  
  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

ROOT_URLCONF = 'admin.urls'
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=120),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



DATABASES_LIST = [
    {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }

    },
]

DATABASES = DATABASES_LIST[0]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = ( ( 'd-m-Y' ))
DATE_INPUT_FORMATS = ( ('%d-%m-%Y'),)
DATETIME_FORMAT = (( 'd-m-Y H:i' ))
DATETIME_INPUT_FORMATS = (('%d-%m-%Y %H:%i'),)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = Path.joinpath(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS
# Ví dụ cấu hình cho việc sao lưu vào thư mục 'backups/'
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_CLEANUP_KEEP = True
DBBACKUP_CLEANUP_KEEP_NUMBER = 3  # Số lượng bản sao lưu giữ lại
DBBACKUP_STORAGE_OPTIONS = {
    'location': '/root/myproject/backup/',
}

def custom_backup_filename(databasename, servername, extension,datetime, content_type):
    formatted_datetime = dt.now().strftime('%Y-%m-%d') 
    return f"{formatted_datetime}.{extension}"

DBBACKUP_FILENAME_TEMPLATE = custom_backup_filename

CRONJOBS = [
    ('00 0 1,15 * *', 'admin.backup.backup_and_upload_to_dropbox'), # Chạy vào ngày 1 và 15 hàng tháng
]

