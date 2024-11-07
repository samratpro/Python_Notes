### 00. Install Dependency
```bash
 pip install django-ckeditor, django-ckeditor-5
 pip install pillow
```
### 01. settings.py 
CK
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
CK-5
```py

INSTALLED_APPS = [
    'django_ckeditor_5',
    'ckeditor_uploader',
]


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

customColorPalette = [
     {
         'color': 'hsl(4, 90%, 58%)',
         'label': 'Red'
     },
     {
         'color': 'hsl(340, 82%, 52%)',
         'label': 'Pink'
     },
     {
         'color': 'hsl(291, 64%, 42%)',
         'label': 'Purple'
     },
     {
         'color': 'hsl(262, 52%, 47%)',
         'label': 'Deep Purple'
     },
     {
         'color': 'hsl(231, 48%, 48%)',
         'label': 'Indigo'
     },
     {
         'color': 'hsl(207, 90%, 54%)',
         'label': 'Blue'
     },
 ]

CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_CONFIGS = {
  'default': {
      'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                  'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

  },
  'extends': {
      'blockToolbar': [
          'paragraph', 'heading1', 'heading2', 'heading3',
          '|',
          'bulletedList', 'numberedList',
          '|',
          'blockQuote',
      ],
      'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
      'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                  'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                  'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                  'insertTable',],
      'image': {
          'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                      'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
          'styles': [
              'full',
              'side',
              'alignLeft',
              'alignRight',
              'alignCenter',
          ]

      },
      'table': {
          'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
          'tableProperties', 'tableCellProperties' ],
          'tableProperties': {
              'borderColors': customColorPalette,
              'backgroundColors': customColorPalette
          },
          'tableCellProperties': {
              'borderColors': customColorPalette,
              'backgroundColors': customColorPalette
          }
      },
      'heading' : {
          'options': [
              { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
              { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
              { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
              { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
          ]
      }
  },
  'list': {
      'properties': {
          'styles': 'true',
          'startIndex': 'true',
          'reversed': 'true',
      }
  }
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # Possible values: "staff", "authenticated", "any"
```

### 02. urls.py ( Project Dir)
CK
```py
urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
```
CK 5
```py
urlpatterns = [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
```
### 03. models.py (CK)
CK
```py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    content = RichTextUploadingField(blank=True, null=True)
```
CK - 5 
```py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Article(models.Model):
    title=models.CharField('Title', max_length=200)
    text=CKEditor5Field('Text', config_name='extends')
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
