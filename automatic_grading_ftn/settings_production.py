# Production settings

from settings import *

DEBUG = TEMPLATE_DEBUG = False

DATABASES['default']['name'] = '/home/grading/database.db'

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = '/home/gajop/grading/uploads'
STATIC_ROOT = '/home/gajop/grading/webservice/static'
LOGGING['handlers']['logfile']['filename'] = 'grading.log'
