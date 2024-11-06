from celery import Celery

celery_app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['tasks']
)

celery_app.conf.task_routes = {
    'tasks.example_task': 'main-queue',
}

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

if __name__ == '__main__':
    celery_app.start()
