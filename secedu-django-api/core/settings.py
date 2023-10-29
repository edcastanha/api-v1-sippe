import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'MYSECRET', '78cdsvc7sdavb07nvar87ynbdravs7by87yvb7ab09se7vybrsd7vyd9'
    )

PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('PG_PASSWORD', 'secedu123')
PG_DATABASE = os.environ.get('PG_DATABASE', 'secedu')
PG_PORT = os.environ.get('PG_PORT', '5432')

RBMQ_HOST = os.environ.get('RBMQ_HOST', 'localhost')
RBMQ_PORT = os.environ.get('RBMQ_PORT', '5672')
RBMQ_USER = os.environ.get('RBMQ_USER', 'guest')
RBMQ_PASS = os.environ.get('RBMQ_PASS', 'guest')
BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

DATASET_PATH  = os.path.join(BASE_DIR, os.environ.get('DATASET_PATH', 'dataset'))
FTP_PATH  = os.path.join(BASE_DIR, os.environ.get('FTP_PATH', 'ftp'))
CAPTURE_PATH  = os.path.join(BASE_DIR, os.environ.get('CAPTURE_PATH', 'media/capturas/'))

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

ALLOWED_HOSTS =os.environ.get('ALLOWED_HOSTS').split(',')

# Application definition
INSTALLED_APPS = [
    # General use templates & template tags (should appear first)
    #'adminlte3',
     # Optional: Django admin theme (must be before django.contrib.admin)
    #'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'rest_framework.apps.RestFrameworkConfig',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    # Apps
    'core.cadastros.apps.CadastrosConfig',
    'core.cameras.apps.CamerasConfig',
    'core.webApp.apps.WebappConfig',
]

LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# DEBUG = True
DEBUG = os.environ.get('MYDEBUG', False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PG_DATABASE,
        'USER': PG_USER,
        'PASSWORD': PG_PASSWORD,
        'HOST': PG_HOST,
        'PORT': PG_PORT,
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000 # Define um tamanho maior, se necessário.
DATA_UPLOAD_MAX_MEMORY_SIZE = 6242880 

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


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CELERY SETTINGS
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_BROKER_URL = BROKER_URL
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
#BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Apenas adicione o pickle a esta lista se o seu broker estiver protegido
# contra acessos não desejados (ver userguide/security.html)
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'

# Permite que os atributos de resultados de tarefas disparadas 
# (nome, args, kwargs, worker, retries, queue, delivery_info) 
# sejam escritos no backend.
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'