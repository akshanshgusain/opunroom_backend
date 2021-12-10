from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

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


# Create your models here.

class Community(models.Model):
    address = models.CharField(verbose_name='Address', max_length=30, unique=False, blank=True)

    # Since we have both OneToOne and ManyToMany relations with the same Mdole(Account) we need to add related_name to
    # either of them
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_id')

    date_joined = models.DateTimeField(verbose_name='Date joined',
                                       auto_now_add=True)  # auto_now_add save date only while creating an object

    name = models.CharField(max_length=100, blank=False, null=False)
    profile_image = models.ImageField(max_length=255, upload_to=profile_picture_upload_location, null=True, blank=True,
                                      default=default_profile_picture_upload_location)
    cover_image = models.ImageField(max_length=255, upload_to=profile_cover_upload_location, null=True, blank=True,
                                    default=default_cover_picture_upload_location)

    class Privacy(models.TextChoices):
        PRIVATE = 1, _('Private')
        PUBLIC = 2, _('Public')

    privacy = models.CharField(max_length=5, choices=Privacy.choices, default=Privacy.PUBLIC)

    community_folks = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def get_privacy(self) -> Privacy:
        return self.Privacy[self.privacy]

    # Requires Function
    def __str__(self):
        return f'{self.name}, {self.created_by}, {self.privacy}'
