""" When Tasking from Model, View never wait for task """

# perform_job.py
def perform_job(keyword):
    print(f"Processing keyword: {keyword.keyword} for user: {keyword.user_info.user}")
    # Add your specific job logic here



from django.db import models
from .perform_job import perform_job  # Import perform_job function
class UserInfo(models.Model):
    user = models.CharField(max_length=100, unique=True)

class Keyword(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Pending')

    class Meta:
        ordering = ['id']

    @classmethod
    def enqueue_keyword(cls, user, keyword):
        user_info, created = UserInfo.objects.get_or_create(user=user)
        cls.objects.create(user_info=user_info, keyword=keyword)

    @classmethod
    def process_next_keyword(cls, user):
        user_info = UserInfo.objects.get(user=user)
        next_keyword = cls.objects.filter(user_info=user_info, status='Pending').first()
        if next_keyword:
            next_keyword.status = 'Running'
            next_keyword.save()
            perform_job(next_keyword)
            next_keyword.status = 'Completed'
            next_keyword.save()

    @classmethod
    def process_user_queue(cls, user):
        pending_keywords_exist = True
        while pending_keywords_exist:
            pending_keyword = cls.objects.filter(user_info__user=user, status='Pending').first()
            if pending_keyword:
                cls.process_next_keyword(user)
            else:
                pending_keywords_exist = False
            time.sleep(5)  # Adjust sleep duration as needed
