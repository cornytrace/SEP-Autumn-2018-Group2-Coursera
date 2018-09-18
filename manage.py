#!/usr/bin/env python
import os
import sys
import warnings

import dotenv

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        dotenv.read_dotenv(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eit_dashboard.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)
