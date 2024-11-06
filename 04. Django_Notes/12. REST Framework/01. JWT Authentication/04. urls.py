# Core.urls / Project.urls *******************************
urlpatterns = [
    path('api/', include('api.urls')),
]
# App.urls ***********************

from django.urls import path
from .views import (LoginView, RegisterView, ForgetPasswordView, SendCodeView, SetNewPasswordView, DataListView)

urlpatterns = [
    path('api_login/', LoginView.as_view(), name='api_login'),
    path('api_register/', RegisterView.as_view(), name='api_register'),
    path('api_forget_password/', ForgetPasswordView.as_view(), name='api_forget_password'),
    path('api_sendcode/', SendCodeView.as_view(), name='api_sendcode'),
    path('api_setnew_password/', SetNewPasswordView.as_view(), name='api_setnew_password'),
  
    path('api_datalist_view/', DataListView.as_view(), name='api_datalist_view'),
]
