## Install Module and Create App
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
python manage.py startapp api
```
## settings.py
```py
from datetime import timedelta

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]


# REST Framework configurations
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
CORS_ALLOW_ALL_ORIGINS = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```
## project's urls.py
```py
urlpatterns = [
    path('api/', include('api.urls')),
]
```
## api app urls.py
```py
from django.urls import path
from .views import (LoginView, RegisterView, ForgetPasswordView, SendCodeView, SetNewPasswordView)

urlpatterns = [
    path('apilogin/', LoginView.as_view(), name='apilogin'),
    path('apiregister/', RegisterView.as_view(), name='apiregister'),
    path('apiforgetpassword/', ForgetPasswordView.as_view(), name='apiforgetpassword'),
    path('apisendcode/', SendCodeView.as_view(), name='apisendcode'),
    path('apisetnewpassword/', SetNewPasswordView.as_view(), name='apisetnewpassword'),
]
```
