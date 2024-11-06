from django.core.files.base import ContentFile

def save_generated_images(self_model, img_url_list):
    try:
      for image_url in img_url_list:
          model_field_name = f"image_url{i}"  # Model
          image_content = requests.get(image_url).content
          image_field = getattr(self_model, image_field_name)
          image_field.save(f"img{str(self_model.pk)}{str(i)}.jpg", ContentFile(image_content), save=False)
      self_model.save()
    except Exception as e:
        logger.error("Error saving images: " + str(e))
