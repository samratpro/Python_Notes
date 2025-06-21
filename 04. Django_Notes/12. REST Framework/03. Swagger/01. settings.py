

INSTALLED_APPS = [
    "rest_framework",
    "drf_yasg",
    'drf_spectacular',
]


REST_FRAMEWORK = {
         'DEFAULT_AUTHENTICATION_CLASSES': [
             'rest_framework.authentication.TokenAuthentication',
             'rest_framework.authentication.SessionAuthentication',
         ],
         'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_PERMISSION_CLASSES': [
                'rest_framework.permissions.AllowAny',
            ],
     }
