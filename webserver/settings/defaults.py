import os
from django.contrib import messages

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SETTINGS_DIR)
BUILDOUT_DIR = os.path.dirname(PROJECT_DIR)
VAR_DIR = os.path.join(BUILDOUT_DIR, "var")

##########################################################################
#
# Secret settings
#
##########################################################################
# If a secret_settings file isn't defined, open a new one and save a
# SECRET_KEY in it. Then import it. All passwords and other secret
# settings should be stored in secret_settings.py. NOT in settings.py
try:
    from secret_settings import *
except ImportError:
    print "Couldn't find secret_settings file. Creating a new one."
    secret_settings_loc = os.path.join(SETTINGS_DIR, "secret_settings.py")
    with open(secret_settings_loc, 'w') as secret_settings:
        secret_key = ''.join([chr(ord(x) % 90 + 33) for x in os.urandom(40)])
        secret_settings.write("SECRET_KEY = '''%s'''\n" % secret_key)
    from secret_settings import *

##########################################################################
#
# Administrative settings
#
##########################################################################

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


##########################################################################
#
#  Authentication settings
#
##########################################################################

# Sets up the get_profile() method for User
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

# When a user successfully logs in, redirect here by default
LOGIN_REDIRECT_URL = '/profile/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Require that users who are signing up provide an email address
ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_EMAIL_VERIFICATION  is set in development.py and production.py

ACCOUNT_EMAIL_SUBJECT_PREFIX = "[SIG-Game]"

# Try to pull username/email from provider.
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'openid': {
        'SERVERS': [
            {'id': 'yahoo',
             'name': 'Yahoo',
             'openid_url': 'http://me.yahoo.com'},
            {'id': 'google',
             'name': 'Google',
             'openid_url': 'https://www.google.com/accounts/o8/id'},
        ]
    }
}

# Django Guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/profile/%s/" % u.username,
}


##########################################################################
#
# Bleach settings
#
##########################################################################
import bleach

ALLOWED_HTML_TAGS = bleach.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'p', 'img']

ALLOWED_HTML_ATTRS = bleach.ALLOWED_ATTRIBUTES
ALLOWED_HTML_ATTRS.update({
        'img': ['src', 'alt'],
        })

##########################################################################
#
# Crispy settings
#
##########################################################################

CRISPY_TEMPLATE_PACK = 'bootstrap'


##########################################################################
#
# Celery settings
#
##########################################################################
import djcelery
djcelery.setup_loader()

try:
    BROKER_URL
except NameError:
    BROKER_URL = 'django://'

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

##########################################################################
#
# Greta settings
#
##########################################################################

GRETA_ROOT_DIR = os.path.join(VAR_DIR, "repos")
GRETA_ROOT_TEST_DIR = os.path.join(VAR_DIR, "test_repos")
GRETA_ARCHIVE_DIR = os.path.join(VAR_DIR, "archives")
GRETA_PAGE_COMMITS_BY = 10

##########################################################################
#
# Git settings
#
##########################################################################

# These settings should be included in secret_settings.py

# GIT_HOST = None
# GIT_PORT = None
GIT_PROTOCOL = 'ssh'


##########################################################################
#
# Testing settings
#
##########################################################################

# Sets the testrunner to Nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


##########################################################################
#
# Blog settings
#
##########################################################################

# Disable the WYSIWIG editor and use a markup language instaead.
ZINNIA_MARKUP_LANGUAGE = 'markdown'

# Disable comments and pingbacks immediately
ZINNIA_AUTO_CLOSE_COMMENTS_AFTER = 0
ZINNIA_AUTO_CLOSE_PINGBACKS_AFTER = 0

ZINNIA_PING_DIRECTORIES = ()
ZINNIA_PING_EXTERNAL_URLS = False


##########################################################################
#
# Messages settings
#
##########################################################################

# Change the default messgae tags to play nice with Bootstrap
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-debug',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-error',
}


##########################################################################
#
# Database settings
#
##########################################################################

# Should be overridden by development.py or production.py
DATABASES = None

# Add project/fixtures to the list of places where django looks for
# fixtures to install.
FIXTURE_DIRS = (
    os.path.join(PROJECT_DIR, "fixtures"),
)


##########################################################################
#
# Cache settings
#
##########################################################################

CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = 'web_cache'

##########################################################################
#
# Location settings
#
##########################################################################

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True


##########################################################################
#
# Static files settings
#
##########################################################################
MEDIA_ROOT = os.path.join(VAR_DIR, "uploads")
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_DIR, "static")
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


##########################################################################
#
# Template settings
#
##########################################################################

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # for django-admin-tools and zinnia
    'django.core.context_processors.request',

    # Optional for Zinnia
    'zinnia.context_processors.version',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)


##########################################################################
#
# Middleware settings
#
##########################################################################

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)


##########################################################################
#
# URL settings
#
##########################################################################

ROOT_URLCONF = 'webserver.urls'


##########################################################################
#
# Installed apps settings
#
##########################################################################

INSTALLED_APPS = (
    # Django AllAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid',

    # Django Admin Tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',  # For serving docs and other flat pages

    # django-crispy-forms
    'crispy_forms',

    # Zinnia
    'tagging',
    'mptt',
    'zinnia_bootstrap',
    'zinnia',

    # Competition app
    'competition',

    # Git app
    'greta',

    # API stuff
    'piston',

    'webserver.home',
    'webserver.profiles',
    'webserver.codemanagement',
    'webserver.hermes',

    'gunicorn',                 # Adds gunicorn management commands
    'guardian',
    'djcelery',                 # Django celery
    'kombu.transport.django',
    'raven.contrib.django.raven_compat',  # Sentry client
    'django_extensions',
    'django_nose',
    'south'
)


##########################################################################
#
# Logging settings
#
##########################################################################

# Check development.py or production.py for specific logging settings.
LOGGING = None
