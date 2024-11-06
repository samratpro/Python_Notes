# Install Celery
pip install celery
pip install django-celery-results
pip install redis

# Documentation :  https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django

# Install Redis (if not installed)
# Windows, Download : https://www.memurai.com/
# Macos, Download   : https://redis.io/docs/install/install-redis/install-redis-on-mac-os/
# For Ubuntu
sudo apt update
sudo apt install redis-server
sudo apt-get install redis-server

# >>> redis-server  command to check redis server is running

# Install celery in app section
INSTALLED_APPS = [
    'celery',
    'django_celery_results'
]


# Celery configuration for Redis as the broker
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'      # or 'redis://localhost:6379/0'    -> in live server   'redis://domain_or_ip:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # or 'redis://localhost:6379/0'    -> in live server   'redis://domain_or_ip:6379/0'  
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

'''
CELERY_TASK_ROUTES = {
    'app1.tasks.*': {'queue': 'worker1'},
    'app2.tasks.*': {'queue': 'worker1'},
}
'''
# app1, app2 is app_name & tasks is filename here 
# worker1, worker2 is for terminal

CELERY_TASK_DEFAULT_QUEUE = 'default'

# Need to run and check redis server before run celery
# >>> redis-server


# After setup or update -> navigate to your Django project directory, and run the Celery worker
# Must open a new separate terminal and use these command
# All tasks with celery will show in this tab ---
# celery -A project_name worker -l info                                 # replace project name (-l info or --loglevel=info )
# celery -A project_name worker -l info --concurrency=10 -Q worker1     # Running 10 task in worker1 
# celery -A project_name worker -l info --concurrency=10 -Q worker2     # Running 10 task in worker2

'''
    But need to configure the targeted task
    for _ in range(threads):
        func.delay(arg)
'''

# Debug
# celery -A project_name worker -l debug                                 # replace project name (-l info or --loglevel=info )
# celery -A project_name worker -l debug  --concurrency=10 -Q worker1     # Running 10 task in worker1 
# celery -A project_name worker -l debug  --concurrency=10 -Q worker2     # Running 10 task in worker2
