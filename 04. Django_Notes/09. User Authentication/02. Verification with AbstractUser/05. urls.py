from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('login/', views.login, name='login'),   
    path('logout', views.logout, name='logout'),  
     
    path('register', views.register, name='register'),   
    path('activate/<str:activation_code>/', views.activate_account, name='activate_account'),  
    
    path('forget_password/', views.forget_password, name='forget_password'),
    path('forget_password/confirm/<str:forget_code>/', views.forget_password_confirm, name='forget_password_confirm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
