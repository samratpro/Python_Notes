## Step 1: Debug False in Settings
## Step 2: Configure ngnix configurations
in nginx before location ~ \.well-known
```py
    location /static/ {
        alias /www/wwwroot/service_site/staticfiles/;
        expires 30d;  # Cache static files for 30 days
        access_log off;  # Reduce logging for static files
    }

    # Media files
    location /media/ {
        alias /www/wwwroot/service_site/media/;
        access_log off;
    }

    # Directory verification related settings for one-click application for SSL certificate
    location ~ \.well-known{
        allow all;
    }
```
## Step 3: Create 404.html, 500.html page
## Step 4: Create 404.html, 500.html page
## Step 5: Run collectstatic migration
```py
env/bin/python3 manage.py collectstatic --noinput
```
## Step 6: For Custom 404
```PY
# core/views.py
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)
```
