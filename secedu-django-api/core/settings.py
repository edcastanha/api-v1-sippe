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
    'jazzmin',
    #Default
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
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    #os.path.join(BASE_DIR, 'staticfiles'),
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



#TEMPLATE ADMIN SETTINGS
JAZZMIN_SETTINGS = {
    # título da janela (será predefinido para current_admin_site.site_title se não estiver presente ou se não existir)
    "site_title": "SecEdu Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "SecEdu",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SecEdu",

    # Logo to use for your site, must be present in static files, used for brand on top left
    #"site_logo": "books/img/logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    #"login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    #"login_logo_dark": None,

    # CSS classes that are applied to the logo above
    #"site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
   # "site_icon": None,

    # Welcome text on the login screen
    #"welcome_sign": "Welcome to the library",

    # Copyright on the footer
    "copyright": "SecEdu - GELD Ltd",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    #"search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    #"user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    #"topmenu_links": [

        # Url that gets reversed (Permissions can be added)
    #    {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
    #    {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
    #    {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
    #    {"app": "books"},
    #],

    #############
    # User Menu #
    #############

    # Ligações adicionais a incluir no menu do utilizador no canto superior direito (o tipo de url "app" não é permitido)
    #"usermenu_links": [
    #    {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #    {"model": "auth.user"}
    #],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    #"show_sidebar": True,

    # Whether to aut expand the menu
    #"navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['django_celery_beat', 'django_celery_results', 'django_extensions', ],

    # Ocultar estes modelos ao gerar o menu lateral (e.g auth.user)
    "hide_models": [],

    # Lista de aplicações (e/ou modelos) para basear a ordenação do menu lateral (não é necessário conter todas as aplicações/modelos)
    "order_with_respect_to": ["core.cameras.cameras", "core.cadastros.peaaoas",],

    # Custom links to append to app groups, keyed on app name
    #"custom_links": {
    #    "books": [{
    #        "name": "Make Messages", 
    #        "url": "make_messages", 
    #        "icon": "fas fa-comments",
    #        "permissions": ["books.view_book"]
    #    }]
    #},

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    #"language_chooser": True,
}