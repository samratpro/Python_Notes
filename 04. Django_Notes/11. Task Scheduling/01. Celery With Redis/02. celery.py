# Exact same name `celery.py` in Project Folder

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')   #  ----- Change project_name 

app = Celery('project_name')                                               # ----- Change project_name 

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.task_routes = {
    'app1.tasks.*': {'queue': 'worker1'},
    'app2.tasks.*': {'queue': 'worker2'},
}

# app1, app2 is app_name & tasks is filename here 
# worker1, worker2 is for terminal


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
