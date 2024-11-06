# Setting ------------------------------------------


# App connection..     # Probbaly 33 line
INSTALLED_APPS = [
    'NewApp',
]


ALLOWED_HOSTS = ['*','domain.com']
CSRF_TRUSTED_ORIGINS = [
    'https://domain.com'
]



# Template Connection..
DIRS': [BASE_DIR / 'templates'], # Probbaly 59 line


# Static File Connection..   # Probbaly 123 line
# CSS, JS, Static Icon, Logo etc
# static folder is required
# static images will have in this folder
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles" # for collect static

'''
# This is for Hosted server and When Debug is False after Hosting Django App in Domain
>>> python manage.py collectstatic
- Now configure Project urls.py
- Or collect CSS and from `staticfiles` folder and paste it in `static` folder
- Turn off/on Debug True/False and Restart app It will fix
- If Debug is True then admin CSS won't work in the local Server
- 404.html and Debug is false for 404 page
'''

# For media support, also need to create ` media  ` in media >>> ` images ` folder where have manage.py 
# Also, need to Configure urls.py file for ` media support ` 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


TIME_ZONE = 'Asia/Dhaka'

# Postgresql database  # Probbaly 78 line
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'samrat',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
    }
}



# Django Logger ---- ** It is most important when application move in server
# path - Need to create ` logs ` folder and `console.log` file in folder
# logs / console.log  

import os
from django.conf import settings

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(Path(settings.BASE_DIR) / 'logs' / 'console.log'),
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}


# in views.py or any other files
import logging
logger = logging.getLogger("django")
logger.info('Message')

