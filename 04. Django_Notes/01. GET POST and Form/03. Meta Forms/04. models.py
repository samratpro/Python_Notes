from django.db import models


class ContactFormModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
