# Django settings for swts project.
import os.path

# with trailing /
BASE_URL = '/'


BASE_DIR = os.path.join(os.path.curdir,
                        os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME   = os.path.join(BASE_DIR, 'swts.db')
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
MEDIA_ROOT = os.path.join(BASE_DIR, 'site_media')

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"swts.context_processors.url_info",
        "swts.context_processors.registry"
        )



TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

ROOT_URLCONF = 'swts.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'mptt',
    'swts.agenda',
    'swts.tasks',
    'swts.kb',
    'swts.cid',
)

LOGIN_REDIRECT_URL = BASE_URL
LOGIN_URL = BASE_URL + 'login/'
LOGOUT_URL = BASE_URL + 'logout/'


#-----------------------------------------#
#            Auth stuff                   #
#-----------------------------------------#

AUTHENTICATION_BACKENDS = (
    # 'swts.auth.adldap.ADLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_AD_DOMAIN      = 'policlinico.org'
AUTH_AD_SERVER      = 'mercurio.policlinico.org'
AUTH_AD_PORT        = 389
AUTH_AD_USETLS      = True
AUTH_AD_CACERTFILE  = '/etc/ssl/certs/plc-ca.pem'
AUTH_AD_SEARCHDN    = 'dc=policlinico,dc=org'
AUTH_AD_FILTER      = 'memberOf=CN=Sistemisti,OU=utenti di servizio,OU=CED,DC=policlinico,DC=org'
AUTH_AD_CREATEUSER  = True  # False

