"""
WSGI config for chatstack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""


# import os

import django.core.handlers.wsgi
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatstack.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


# os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
app = django.core.handlers.wsgi.WSGIHandler()