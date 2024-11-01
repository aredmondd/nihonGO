"""
WSGI config for nihonGO project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'nihonGO' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nihonGO.settings')
nihonGO_application = get_wsgi_application()

# Set the default settings module for the 'DjangoChat' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoChat.settings')
DjangoChat_application = get_wsgi_application()

# Define an application dispatcher to route requests to the appropriate application
class ApplicationDispatcher:
    def __init__(self, apps):
        self.apps = apps

    def __call__(self, environ, start_response):
        host = environ.get('HTTP_HOST', '')
        if 'djangochat' in host:
            return self.apps['DjangoChat'](environ, start_response)
        else:
            return self.apps['nihonGO'](environ, start_response)

# Create the WSGI application dispatcher
application = ApplicationDispatcher({
    'nihonGO': nihonGO_application,
    'DjangoChat': DjangoChat_application,
})
