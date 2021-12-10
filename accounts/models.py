from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from community.models import Community
from friend.models import FriendList

''' Helper Functions'''


# File name is optional
def profile_picture_upload_location(self, filename='di'):
    file_path = f'accounts/profile_pictures/{str(self.pk)}-{filename}.png'
    return file_path


def default_profile_picture_upload_location():
    return 'opundoor/img/default_profile_image.png'


# File name is optional
def profile_cover_upload_location(self, filename='ci'):
    file_path = f'accounts/profile_cover_picture/{str(self.pk)}-{filename}.png'
    return file_path


def default_cover_picture_upload_location():
    return 'opundoor/img/default_cover_image.png'


''' Managers '''


# create a new user
# create a new super-user

class MyAccountManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(
            username=username,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        user = self.create_user(
            username=username,
            phone_number=phone_number,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


''' Models '''


class Account(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)  # auto_now_add save date only while creating an object
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # Required Fields
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Custom Fields
    f_name = models.CharField(max_length=50, default='First Name')
    l_name = models.CharField(max_length=50, default='Last Name')
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=256, null=True, blank=True, unique=False)
    profile_image = models.ImageField(max_length=255, upload_to=profile_picture_upload_location, null=True, blank=True,
                                      default=default_profile_picture_upload_location)
    cover_image = models.ImageField(max_length=255, upload_to=profile_cover_upload_location, null=True, blank=True,
                                    default=default_cover_picture_upload_location)

    class Privacy(models.TextChoices):
        PRIVATE = 1, _('Private')
        PUBLIC = 2, _('Public')

    privacy = models.CharField(max_length=5, choices=Privacy.choices, default=Privacy.PRIVATE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyAccountManager()

    def get_privacy(self) -> Privacy:
        return self.Privacy[self.privacy]

    # Requires Function
    def __str__(self):
        return f'{self.username}, {self.f_name} {self.l_name}, {self.phone_number}'

    # Required Permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class OTP(models.Model):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text="Number of OTP Sent")
    validated = models.BooleanField(default=False,
                                    help_text="If it is true that means user have validated OTP correctly in second API")
    otp_session_id = models.CharField(max_length=120, null=True, default="")
    username = models.CharField(max_length=20, blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.phone_number} is sent {self.otp} with session ID: {self.otp_session_id}'


''' Receivers '''


@receiver(post_save, sender=Account)
def user_save(sender, instance, **kwargs):
    FriendList.objects.get_or_create(user=instance)
