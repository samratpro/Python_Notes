from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _  # different languages translated 

'''
For multiple users we can create Users two way :
________________________________________________________________________________
01. First way in Custom user example: `is_student` and `is_teacher`
02. Second way Two Custom Model with Custom/Default User Model Forigen Key
    These need to Register in Admin
________________________________________________________________________________
'''

''' When uses user custom user, user model shold be '''
from django.conf import settings
class ModelName(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL)

class UserManager(BaseUserManager):
    """User manager action for, superuser and multiple user type"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)       # is_active False for Email Verification 
        extra_fields.setdefault('is_teacher', False)
        extra_fields.setdefault('is_student', False)
        user = self.model(email=email, **extra_fields)    # Instead of username, here we used email pass none here also need *** auth_email.py 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_teacher(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_teacher', True)
        return self.create_user(email, password, **extra_fields)

    
    def create_student(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_student', True)
        return self.create_user(email, password, **extra_fields)

    
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_teacher', True)
        extra_fields.setdefault('is_student', True)
        
        ''' These are optional '''
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_teacher') is not True:
            raise ValueError('Superuser must have is_teacher = True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        ''' These are optional '''
        
        return self.create_user(email, password, **extra_fields)



class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no extra fields required for creating a user
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    credit = models.IntegerField(default=0)
    
    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.activation_code = ''
        self.save()
    
    def save(self, *args, **kwargs):        # For email Lowercase
        if self.email:
            self.email.lower()
        super(AppUser, self).save(*args, **kwargs)


# If user has any task
'''
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='assigned_tasks')  # related name is for avoid same usermodle using error of multiple time
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='created_tasks')

class TeacherGroup(Group):
    class Meta:
        proxy = True

class StudentGroup(Group):
    class Meta:
        proxy = True

class TaskPermission(Permission):
    class Meta:
        proxy = True
        default_permissions = ()
        permissions = (
            ('can_create_task', 'Can create task'),
            ('can_remove_student', 'Can remove student'),
        )
'''


# Alternate Way :  Create a Universal User Model and Create multiple Type Profile
'''
class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    
    # Remove related_name for groups and user_permissions
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)
    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.activation_code = ''
        self.save()

    def save(self, *args, **kwargs):
        # For email lowercase
        self.email = self.email.lower()
        super(AppUser, self).save(*args, **kwargs)

class Teacher(models.Model):
    user_profile = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(AppUser, related_name='teachers')           # Teachers have multiple students.
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def activate(self):
        self.user_profile.activate()

class Student(models.Model):
    user_profile = models.ForeignKey(AppUser, on_delete=models.CASCADE) 
    teachers = models.ManyToManyField(AppUser, related_name='students')      # Students have multiple teachers.
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def activate(self):
        self.user_profile.activate()
'''
