from huey import crontab
from huey.contrib.djhuey import periodic_task

@periodic_task(crontab(hour=23, minute=0))
def my_periodic_task():
    # Code to perform daily cleanup tasks goes here.


# Run task
# Run command  ------------
# python manage.py run_huey
