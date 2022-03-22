from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save

from . import create_random_id

class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email or username:
            ValueError('Users must have an email address')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    id = models.CharField(primary_key=True, default=create_random_id, max_length=32)
    email = models.EmailField('メールアドレス', max_length=255, unique=True,)
    username = models.CharField('ユーザー名', max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField('ファーストネーム', default='', max_length=20, blank=True)
    last_name = models.CharField('ラストネーム', default='', max_length=20, blank=True)
    zipcode = models.CharField('郵便番号', default='', max_length=20, blank=True)
    prefecture = models.CharField('都道府県', default='', max_length=50, blank=True)
    address1 = models.CharField('住所1', default='', max_length=50, blank=True)
    address2 = models.CharField('住所2', default='', max_length=50, blank=True)
    phone_num = models.CharField('電話番号', default='', max_length=20, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.first_name

@receiver(post_save, sender=User)
def create_profile(sender, *args, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])