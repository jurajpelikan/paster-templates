import os
import sys 
import site 

ALLDIRS = ['env/lib/python2.6/site-packages', 'project', '']

# Absolute paths.
base_path = os.path.join(os.path.dirname(__file__), '..')
ALLDIRS = [ os.path.join(base_path, path) for path in ALLDIRS ]

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 


os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)

