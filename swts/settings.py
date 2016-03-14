# Django settings for swts project.

# idiom to get path of project
import os
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# with trailing /
BASE_URL = '/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME   = os.path.join(PROJECT_PATH, 'swts.db')
DATABASE_USER   = ''
DATABASE_PASSWORD = '' 
DATABASE_HOST = '' # localhost
DATABASE_PORT = ''

# Local time zone for this installation.
TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'site_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = BASE_URL + 'site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = BASE_URL + 'media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e4f102os6mh5kxxsp6r%wh+0ro!who!wgae6z1zp3gul2w1$zn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'swts.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'mptt',

    'agenda',
    'tasks',
    'kb',
    'cid',
)

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL='login'
LOGOUT_URL='home'


#-----------------------------------------#
#            Auth stuff                   #
#-----------------------------------------#

AUTHENTICATION_BACKENDS = (
    # 'swts.auth.adldap.ADLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_AD_DOMAIN      = 'contoso.org'
AUTH_AD_SERVER      = 'contoso.org'
AUTH_AD_PORT        = 389
AUTH_AD_USETLS      = True
AUTH_AD_CACERTFILE  = '/etc/ssl/certs/ca.pem'
AUTH_AD_SEARCHDN    = 'dc=contoso,dc=org'
AUTH_AD_FILTER      = 'memberOf=CN=MyUSers,DC=Contoso,DC=Org'
AUTH_AD_CREATEUSER  = True  # False


