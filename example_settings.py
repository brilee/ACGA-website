import os

DEBUG = True
TEMPLATE_DEBUG = True

#SESSION_COOKIE_SECURE = True


ADMINS = (
    ('Some Person', "someperson@foobar.com"),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite',
    }
}

TIME_ZONE = 'America/New_York'
USE_TZ = False
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
ADMIN_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media', 'admin')

WEB_URL = '127.0.0.1:8000'
MEDIA_URL = os.path.join(WEB_URL, 'site_media', '')
STATIC_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = '3zblahblahblahblahblahblahblahblahblahblahblahblah'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.contrib.auth.context_processors.auth',
    'CGL.context_processors.sidebar_CGL',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PROJECT_ROOT, 'templates/ACGA'),
    os.path.join(PROJECT_ROOT, 'templates/CGL'),
    os.path.join(PROJECT_ROOT, 'templates/captain'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'CGL',
    'django.contrib.redirects',
    'south',
    'email_obfuscator',
    'registration'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1
ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = "CGL.Player"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'notarealemail@gmail.com'
# EMAIL_HOST_PASSWORD = "nottherealpassword"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
