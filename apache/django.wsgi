import os, sys
sys.path.append('/home/cole/Webs')

os.environ['DJANGO_SETTINGS_MODULE'] = 'CGA.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
