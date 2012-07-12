
# Usernames / passwords::
#
# (To generate a new password hash:
# import bcrypt
# hashed = bcrypt.hashpw('password', bcrypt.gensalt(12))
# # -- adjust value in gensalt for available CPU power...)
CUBE_AUTH = {
    'read': (
        '$2a$12$2xv8/PUuYW6yQGjPOQN7l./gbny1MskLYQnlrbvZNSr1el9NprJqa',  # Username
        '$2a$12$p1Y1/08tElCxmUDSUasAAeTKzcpWhICQf8gcEdkIAL4rjUyKCWMz6'   # Password
    ),
    'write': (
        '$2a$12$re7bQximlvz0hcJCHnS.nOd11jIq.XsK8aSXTIQGFiXnIQ0WvIw5m',  # Username
        '$2a$12$kj2ftlD4U/m0z333dFixPuyvoyIohXy8hIbZDRk3TixYRtt7x/vlO'   # Password
    ),
}

# Slightly arbitrary (inherited) bounding box for thumbnails
THUMBNAIL_SIZE = (250, 187)

DEFAULT_TERMS_TEXT = """Contacts-
Company-
Address-
Email-
Ph No-
Hire Fee (inclusive of VAT, if applicable) -
Financial Deal (%/fee/split etc)-
Deposit paid before the night (p/h only) -
Amount needed to be collected (p/h only) -
Special Terms -
Tech needed -
Additonal Info -"""

DEFAULT_MUGSHOT = "/static/members/default_mugshot.gif"

# Following settings are used by the import script, can be discarded when
# switch-over is finalised.
IMPORT_SCRIPT_USER = 'toolkitimport'
IMPORT_SCRIPT_DATABASE = 'toolkitimport'

###############################################################################
#
# Below here are Django settings
#

# Custom:
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

APPEND_SLASH = True

# Django settings for cube project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'
        'NAME': 'cube',                      # Or path to database file if using sqlite3.
        'USER': 'cube',                      # Not used with sqlite3.
        'PASSWORD': 'hialpabg',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False  # True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Following are defined in settings_*.py
## Absolute filesystem path to the directory that will hold user-uploaded files.
## Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = os.path.join(APP_ROOT,'media')
#
## URL that handles the media served from MEDIA_ROOT. Make sure to use a
## trailing slash.
## Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = '/media/'
#
## Absolute path to the directory static files should be collected to.
## Don't put anything in this directory yourself; store your static files
## in apps' "static/" subdirectories and in STATICFILES_DIRS.
## Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(APP_ROOT,'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Where to store messages:
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's62e_vyvEh+asx_v!85p&r*9n$46_8w3q%51*ceg=-zcnd9mhu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'toolkit.urls'

#TEMPLATE_DIRS = (
#    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#    # Always use forward slashes, even on Windows.
#    # Don't forget to use absolute paths, not relative paths.
#    os.path.join(APP_ROOT, 'templates'),
#)

INSTALLED_APPS = (
    'toolkit.diary',
    'toolkit.members',
    'toolkit.auth',
    # disabled for now;
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'south',
    'django.contrib.markup',
)
