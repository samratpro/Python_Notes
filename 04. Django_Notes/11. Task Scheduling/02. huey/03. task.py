# app_folder/tasks.py

# Must be write code organize way
# Must be seperate functions, instead of using inner function

from huey.contrib.djhuey import task
from huey.contrib.djhuey import db_task

@task()
def content_creation_job(arg1, arg2):
    # Task logic goes here
    pass

# example 2
@db_task()
def my_db_task(param1, param2):
    # Do something with param1 and param2 using the Django database like
    objects=MyModel.objects.filter(name=param1).all()
    pass

# example task 3
@task()
def my_async_task(request):
    # Do something asynchronously, such as send a request to an external API or send an email
    pass

# After setup or update -> navigate to your Django project directory, and run the Celery worker
>>> celery -A project_name worker -l INFO   # replace with your project name
