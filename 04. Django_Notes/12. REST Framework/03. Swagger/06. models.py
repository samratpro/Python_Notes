from django.db import models
from userapp.models import AppUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid


# Software Model (unchanged)
class Software(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    version = models.CharField(max_length=50)
    release_date = models.DateField()
    download_link = models.URLField()
    video_link = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField('SoftwareCategory', related_name='software', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, related_name='created_software')
    max_devices = models.IntegerField(default=3)
    
    def __str__(self):
        return self.name + f", id : {self.id}"


class Device(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    os_version = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(protocol='IPv4')
    mac_address = models.CharField(max_length=17)
    last_login = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('software', 'mac_address')
        indexes = [
            models.Index(fields=['software', 'mac_address', 'is_active']),
        ]

    def __str__(self):
        return f"{self.device_name} ({self.software.name})"

    def clean(self):
        super().clean()
        if Device.objects.filter(software=self.software, mac_address=self.mac_address).exclude(pk=self.pk).exists():
            raise ValidationError("This device is already registered with this software.")

        if self.pk is None:
            active_devices_count = Device.objects.filter(
                software=self.software,
                is_active=True
            ).count()

            if active_devices_count >= self.software.max_devices:
                raise ValidationError(
                    f"Maximum device limit ({self.software.max_devices}) reached for this plan. "
                    "Please deactivate other devices before adding new ones."
                )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk is None or self._state.adding:
            active_devices_count = Device.objects.filter(
                software=self.software,
                is_active=True
            ).count()

            if active_devices_count >= self.software.max_devices:
                raise ValidationError(
                    f"Maximum device limit ({self.software.max_devices}) reached for this plan."
                )

            Notification.create_with_limit(
                user=self.software.created_by,
                message=f"New login detected from {self.device_name} in {self.location or 'unknown location'}.",
                timestamp=timezone.now()
            )

        super().save(*args, **kwargs)
