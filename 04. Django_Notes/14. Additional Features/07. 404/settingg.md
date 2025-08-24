## Step 1: Debug False in Settings
## Step 2: Remove debug if in project urls.py
```py
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
## Step 3: Create 404.html, 500.html page
## Step 4: Create 404.html, 500.html page
## Step 5: Run collectstatic migration
```py
env/bin/python3 manage.py collectstatic --noinput
```
