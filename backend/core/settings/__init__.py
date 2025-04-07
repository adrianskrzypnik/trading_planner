import os

# Defaultowo używamy dev.py, chyba że zmienna DJANGO_SETTINGS_MODULE jest ustawiona
environment = os.environ.get('DJANGO_ENVIRONMENT', 'dev')

if environment == 'prod':
    from .prod import *
else:
    from .dev import *