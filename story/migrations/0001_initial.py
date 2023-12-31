# Generated by Django 3.2.5 on 2021-12-08 12:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import story.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
        ('community', '0005_auto_20211207_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_video', models.URLField(blank=True, max_length=255, null=True)),
                ('duration', models.IntegerField()),
                ('type', models.CharField(choices=[('0', 'Image'), ('1', 'Video')], max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('story_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='story.story')),
                ('story_picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=story.models.user_story_picture_upload_location)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_story_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('story.story',),
        ),
        migrations.CreateModel(
            name='GroupStory',
            fields=[
                ('story_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='story.story')),
                ('story_picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=story.models.group_story_picture_upload_location)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_story_group', to='group.groupt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_story_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('story.story',),
        ),
        migrations.CreateModel(
            name='CommunityStory',
            fields=[
                ('story_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='story.story')),
                ('story_picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=story.models.community_story_picture_upload_location)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_story_community', to='community.community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='community_story_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('story.story',),
        ),
    ]
