# Generated by Django 3.2.5 on 2021-12-09 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_auto_20211207_0050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='group_folks',
            new_name='community_folks',
        ),
    ]
