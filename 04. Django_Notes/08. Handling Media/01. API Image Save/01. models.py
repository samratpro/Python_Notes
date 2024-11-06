from django.db import models

class generated_news_list(models.Model):
    name = models.CharField(max_length=100)
    image_url1 = models.ImageField(upload_to='news_images/', null=True, blank=True)
    image_url2 = models.ImageField(upload_to='news_images/', null=True, blank=True)
    image_url3 = models.ImageField(upload_to='news_images/', null=True, blank=True)

    def __str__(self):
        return self.name
        
    # When delete, also deleting Image from directory
    def delete(self, *args, **kwargs):
        for i in range(1,4):
            field_name = f"image_url{str(i)}"
            image_field = getattr(self, field_name)
            if image_field:
                if os.path.isfile(image_field.path):
                    os.remove(image_field.path)
            else:
                logger.info(f"No image found for {field_name}.")
        super().delete(*args, **kwargs)
