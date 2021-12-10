from django.conf import settings
from django.db import models

# Create your models here.
from accounts.models import Account


class GroupT(models.Model):
    # Since we have both OneToOne and ManyToMany relations with the same Mdole(Account) we need to add related_name to either of them
    group_founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_founder')
    group_title = models.CharField(max_length=20, blank=False, null=False, unique=True)
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='last update', auto_now=True)
    group_folks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_folks')

    def __str__(self):
        return f'{self.group_title}'
