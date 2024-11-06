# Models.py
from django.db import models
class InfoBulkModel(models.Model):
    user = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

#views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import InfoBulkModel

def submit_keywords(request):
    if request.method == 'POST':
        keyword_list = request.POST.get('keywords', '').split(',')
        user = request.user  # Replace with your authentication logic
        for keyword in keyword_list:
            InfoBulkModel.objects.create(user=user, keyword=keyword.strip(), status='Pending')

        return HttpResponse("Keywords submitted successfully!")
    else:
        return render(request, 'submit_keywords.html')

# task.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InfoBulkModel

# This function will perform the job when a keyword becomes 'Pending'
def perform_job(pending_keyword):
    # Your job logic here
    print(f"Performing job for keyword: {pending_keyword}")

# Define a signal receiver
@receiver(post_save, sender=InfoBulkModel)
def keyword_status_changed(sender, instance, created, **kwargs):
    if created and instance.status == 'Pending':
        perform_job(instance.keyword)
