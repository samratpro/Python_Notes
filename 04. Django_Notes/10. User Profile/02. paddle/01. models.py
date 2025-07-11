from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone

# ****************  Subscriptions Packages
class CreditPackage(models.Model):
    name = models.CharField(max_length=255, default='Basic')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    credits = models.IntegerField(default=50000)
    days = models.IntegerField(default=30)
    product_id = models.CharField(max_length=150, null=True, blank=True)   # inputed from paddle
    def __str__(self):
        return self.name

class PaddleToken(models.Model):
    client_token = models.CharField(max_length=150, null=True, blank=True)  # inputed from paddle
    api_key = models.CharField(max_length=150, null=True, blank=True)       # inputed from paddle
    def __str__(self):
        return "Paddle Tokens"



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)       # is_active False for Email Verification 
        user = self.model(email=email, **extra_fields)    # Instead of username, here we used email pass none here
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        
        return self.create_user(email, password, **extra_fields)



class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  
    activation_code = models.CharField(max_length=50, blank=True, null=True)
    password_reset_code = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    credit = models.IntegerField(default=0)
    expire_date = models.DateField(default=timezone.now)
    thread = models.IntegerField(default=1)

    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.activation_code = ''
        self.save()
    
    def save(self, *args, **kwargs):        # For email Lowercase
        if self.email:
            self.email.lower()
        super(AppUser, self).save(*args, **kwargs)

    
    # *****************  Package in user profile with forigenkey
    credit_package = models.ForeignKey(CreditPackage, on_delete=models.SET_NULL, null=True, blank=True)
    # *****************  Credit purchase action, increase credit and expire date
    def purchase_credit(self, credit_package):
        self.credit_package = credit_package
        self.credit += credit_package.credits
        self.expire_date = timezone.now() +  timezone.timedelta(credit_package.days)
        self.save()
        
    # ************  Reducing credit when use it by user
    def use_credit(self, words):
        print(' Outer Words : ', words)
        if self.credit >= words:
            print(' Inner Words : ', words)
            self.credit -= words
            self.save()
            print(' Inner 2 : ', words)
            return True
        print('last words')
        return False
        
   # *********** Credit expiration after expire datae, 3 way credit expire logic perform
   # *********** 01. When user visit profile,
   # *********** 02. When user going to use credit
   # *********** 03. When admin visit user profile
   # *********** 04. or any inetaction with credit, credit_expiration() function perform
    
    def credit_expiration(self):
        if self.credit > 0:
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            if current_date > self.expire_date:
                self.credit = 0
                self.credit.save()
                return True
        return False
