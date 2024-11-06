# Urls.py in Project Folder
urlpatterns = [
    path('api/', include('apiapp.urls')),
] 


# urls.py in App Folder 
from django.urls import path
from .views import *

# GenerateTextView come from views.py
urlpatterns = [
path('generate-text/', GenerateTextView.as_view(), name='generate_text'),
]
