### 00. Install Dependency
```bash
 pip install django-ckeditor
 pip install django-ckeditor-5
 pip install pillow
```
### 01. settings.py
```py

INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
]

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

CKEDITOR_CONFIGS = {
    'default':
        {
            'toolbar': 'full',
            'width': 'auto',
            'extraPlugins': ','.join([
                'codesnippet',
            ]),
        },
}
```
### 02. urls.py ( Project Dir)
```py
urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
```
### 03. models.py
```py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    content = RichTextUploadingField(blank=True, null=True)
```
### 04. views.py
```py
def single_post_view(request, post_id):
    templeate = 'single_post_view.html'
    single_post = SingleKeywordModel.objects.get(pk=post_id)
    context = {'single_post':single_post}
    return render(request, templeate, context=context)
```
### 05. index.html (CK in Frontend)
```html
<script src="{% static 'ckeditor/ckeditor-init.js' %}"></script>
<script src="{% static 'ckeditor/ckeditor/ckeditor.js' %}"></script>


<textarea name="content" id="id_content">{{context.content }}</textarea>
<script>
    CKEDITOR.replace('id_content');
</script>
```
