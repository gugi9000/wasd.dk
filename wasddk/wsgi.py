"""
WSGI config for wasddk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wasddk.settings.dev")
DJANGO_SECRET_KEY = '^7nk)wiwyd3fq0i%xs7xj&vm&f@=4qu)4ow@t60gw)0h#*jv^o'
SECRET_KEY = '^7nk)wiwyd3fq0i%xs7xj&vm&f@=4qu)4ow@t60gw)0h#*jv^o'

application = get_wsgi_application()

