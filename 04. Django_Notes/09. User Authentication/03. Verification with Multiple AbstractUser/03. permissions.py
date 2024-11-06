from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Task, TaskPermission, StudentGroup, TeacherGroup

task_content_type = ContentType.objects.get_for_model(Task)

can_create_task = Permission.objects.get(
    codename='can_create_task',
    content_type=task_content_type,
)

can_remove_student = Permission.objects.get(
    codename='can_remove_student',
    content_type=task_content_type,
)

TeacherGroup.permissions.add(can_create_task, can_remove_student)
StudentGroup.permissions.add(can_create_task)

