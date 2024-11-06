from django.db import models
from tinymce import models as tinymce_models

class MyModel(models.Model):
    my_field = tinymce_models.HTMLField()
