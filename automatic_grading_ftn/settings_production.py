# Production settings

from settings import *

DEBUG = TEMPLATE_DEBUG = False

DATABASES['default']['name'] = '/home/grading/database.db'

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = '/home/grading/uploads'
STATIC_ROOT = '/home/grading/webservice/static/'
STATICFILES_DIRS = ('/home/grading/webservice/static',)
LOGGING['handlers']['logfile']['filename'] = '/var/log/django/grading.log'
