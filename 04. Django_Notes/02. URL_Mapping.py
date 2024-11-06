# URL Mapping in Project URL file-------------------
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('NewApp.urls'))   # Must Have to create urls.py in App folder >> then at least one template render function in views.py 
]  # NewApp is App name here...
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # -------- For collctstatic or admin css
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # -------- For Media Support



# URL Mapping in App URL file----------------------
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  
    path('contactus', views.contactus, name='contactus'),  
    path('article', views.article, name='article'),  
    path('about', views.about, name='about'),  
]

# >>> 404.html and Debug is false for 404 page
