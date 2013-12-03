import os
import sys
import site

site.addsitedir('/home/grading/env-automatic-grading-ftn/lib/python2.6/site-packages')
sys.path.append('/home/grading/')
sys.path.append('/home/grading/webservice')

os.environ['DJANGO_SETTINGS_MODULE'] = 'automatic_grading_ftn.settings_production'

# Activate your virtual env
activate_env=os.path.expanduser("/home/grading/env-automatic-grading-ftn/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
