import os, sys
sys.path.append('/var/www/CGA')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

