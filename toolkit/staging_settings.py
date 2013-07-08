from toolkit.settings_common import *

ALLOWED_HOSTS = ['localhost', 'toolkit', ]

APP_ROOT = '/var/www_toolkit/site'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Enable logging to the logfile (configured in settings_common.py)
LOGGING['root'] = {
    'handlers': ['file'],
    'level': 'DEBUG',
}