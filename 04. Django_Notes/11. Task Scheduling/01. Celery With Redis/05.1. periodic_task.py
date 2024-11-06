# app/task.py
from celery import shared_task
@shared_task
def my_periodic_task():
    # Your periodic task logic here
    print("Executing periodic task...")


# celery.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'my-periodic-task': {
        'task': 'app_name.file_name.my_periodic_task',
        'schedule': crontab(minute='*/15'),  # Execute every 15 minutes
    },
    'add-every-30-seconds': {
        'task': 'app1.tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'multiply-at-noon': {
        'task': 'app2.tasks.multiply',
        'schedule': crontab(hour=12, minute=0),
        'args': (4, 5)
    },
}


# celery -A myproject beat -l info        (Start Celery Beat)
# celery -A myproject worker -B -l info   ( worker and beat together)
