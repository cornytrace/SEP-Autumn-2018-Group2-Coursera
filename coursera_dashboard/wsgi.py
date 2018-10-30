"""
WSGI config for coursera_dashboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import warnings

import dotenv
from django.core.wsgi import get_wsgi_application

with warnings.catch_warnings():
    # django-dotenv raises a warning if the .env file doesn't exist.
    warnings.simplefilter("ignore")
    dotenv.read_dotenv(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
        )
    )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursera_dashboard.settings")

application = get_wsgi_application()
