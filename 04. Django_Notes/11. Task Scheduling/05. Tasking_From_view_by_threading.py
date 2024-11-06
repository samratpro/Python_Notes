#views.py
from .task import *
import threading


def bulkpost(request):
    template = 'bulkpost.html'
    keyword_pending = BulkKeywordModel.objects.filter(status='Pending')
    context = {'keyword_pending': keyword_pending}

    if request.method == 'POST':
        keyword_list = request.POST.get('keyword_list')
        keywords = keyword_list.split('\n')

        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                BulkKeywordModel.objects.create(name=keyword, status='Pending')

                # Start the task scheduler in a separate thread
                scheduler_thread = threading.Thread(target=BulkDatasJob)      #  We can also input BulkDatasJob function's argument
                # scheduler_thread = threading.Thread(target=BulkDatasJob, args=('arg',)) 
                scheduler_thread.start()
        return redirect('bulkpost')
    
    return render(request, template, context=context)

# Models.py
from django.db import models
class InfoBulkModel(models.Model):
    user = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


# task.py
from .models import *
from time import sleep

def BulkDataJob():
    pending_datas = BulkDataModel.objects.filter(status='Pending')
    for data in pending_datas:
        sleep(10)
        data.content = 'Content'
        data.status = 'Completed'
        data.save()

