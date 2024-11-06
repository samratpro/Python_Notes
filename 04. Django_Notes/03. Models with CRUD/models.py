# Import files
from django.db import models           # --------------------------------------------------------- # Global
from django.utils.text import slugify  # --------------------------------------------------------- # For Slug
from django.utils import timezone      # --------------------------------------------------------- # For django server time
from datetime import timedelta         # --------------------------------------------------------- # time calculation


''' When uses user custom user, user model shold be '''
from django.conf import settings
class ModelName(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL)

# Example Model for Blog Post
class PostCetgory(models.Model):
    id = models.AutoField(primary_key=True)  # must be in to avoid future error
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.name)
        super().save(*arg, **kwargs)

class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing serial number, 1,2,3,4,5,6....  must be in to avoid future error
    
    # If user will delete, all associate post will delete for ` on_delete=models.CASCADE `
    # When a model's two field get same ForeignKey the ` related_name='written_by' ` is mendatory to avoid system error

    # Add a dropdown field to the model
    status_choice = [('Publish', 'publish'),('Draft', 'draft'),]
    status = models.CharField( max_length=10, choices=status_choice, default='Publish')

    url = models.URLField(max_length=250)
    # need to use related name when Multiple field uses same inherite modle like ` AppUser `
    author = models.ForeignKey(AppUser, related_name='written_by', on_delete=models.CASCADE, null=True, blank=True)  
    editor = models.ForeignKey(AppUser, related_name='edited_by',on_delete=models.CASCADE, null=True, blank=True) 
    user =  models.ForeignKey(settings.AUTH_USER_MODEL)
    ''' When uses user custom user '''

    author_birth_day = models.DateField(default=timezone.now().date() - timedelta(days=20*365))    # 20 year by defdult
    
    category = models.ForeignKey(PostCetgory, on_delete=models.SET_NULL, null=True, blank=True)   # If user will delete, category never delete
    feature_img = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)    # automatically current date & time when a new instance of the model is created
    expire_date = models.DateField(default=timezone.now)  # timezone.now `date` vs timezone.now() `date and time`
    modified_date = models.DateField(auto_now=True)   # Similar to auto_now_add, it's used with DateTimeField or DateField. It track the last updated 
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        super().save(*arg, **kwargs)


# ********* ForeignKey *** vs *** OneToOneField *** vs *** ManyToManyField ****************
#  Each book can have only one author, but an author can have multiple books.
class Author(models.Model):
    name = models.CharField(max_length=100)
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)  # If author delete All associate Book will delete
    author = models.ForeignKey(Author,on_delete=models.SET_NULL, null=True, blank=True)   # If author delete associate Book will remain

# each Profile is linked to exactly one User, and each User has only one Profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ''' When uses user custom user '''

#  Each Course can have multiple Students enrolled, and each Student can take multiple Courses.
class Student(models.Model):
    name = models.CharField(max_length=100)
class Course(models.Model):
    students = models.ManyToManyField(Student)


# ********** When required Two field both unique at a time ***********
class Vote(models.Model):
    vote_created_by = models.ForeignKey(AppUser, related_name='votes_given', on_delete=models.CASCADE, blank=True, null=True)
    # Each user can give one vote, it can himself or anyone

class VoteRecord(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    student = models.ForeignKey(user, on_delete=models.CASCADE)
    voted_for = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='received_votes')
    voted_at = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ('vote', 'student')  # Ensures each student can give one vote only


# Other Fields ...
integerfield = models.IntegerField(default=3)   # IntegerField
integerfield = models.DecimalField(default=2.5, max_digits=5, decimal_places=2) # Floating and IntegerField Fields , decimal_places = 2.00

# # For JSON Field only
# import jsonfield


# # Create your models here.
# class KeywordData(models.Model):
#     List_Name = models.CharField(max_length=15, null=True)
#     keywords = jsonfield.JSONField(null=True)


#     def __str__(self):
#         return self.List_Name
