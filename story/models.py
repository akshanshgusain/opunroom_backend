from abc import ABC
from enum import Enum

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# 3 Types of story
from community.models import Community
from group.models import GroupT

""" 1 - User Story
    2 - Group Story
    3 - Community Story
"""


# {
#                     "id": "18",
#                     "userid": "17",
#                     "storypicture": "1562576880_1620041572.png",
#                     "duaration": "24",
#                     "type": "1",
#                     "created_at": "2021-05-03 11:32:52",
#                     "updated_at": "2021-05-03 11:32:52",
#                     "status": "1"
#                 }
#
# {
#                     "id": "73",
#                     "groupid": "4",
#                     "userid": "18",
#                     "groupstory": "StoryPicture_1638884340.jpeg",
#                     "duaration": "24",
#                     "type": "1",
#                     "created_at": "2021-12-07 13:39:00",
#                     "updated_at": "2021-12-07 13:39:00",
#                     "status": "1"
#                 }
#
# {
#                     "id": "24",
#                     "networkid": "3",
#                     "userid": "18",
#                     "storypicture": "https://firebasestorage.googleapis.com/v0/b/opunroom.appspot.com/o/Videos%2F1638956557686_opunRooom_vid.mp4?alt=media&token=8a84246f-10c2-4c7b-aafe-1ecec9909fbd",
#                     "duaration": "48",
#                     "type": "1",
#                     "created_at": "2021-12-08 09:42:55",
#                     "updated_at": "2021-12-08 09:42:55",
#                     "status": "1"
#                 }

class StoryType(Enum):
    IMAGE_STORY = 0
    VIDEO_STORY = 1


def user_story_picture_upload_location(self, filename='si'):
    file_path = f'story/user_story/{str(self.user.username)}/{str(self.id)}-{filename}.png'
    return file_path


def group_story_picture_upload_location(self, filename='si'):
    file_path = f'story/group_story/{str(self.group.group_title)}/{str(self.id)}-{str(self.user.username)}-{filename}.png'
    return file_path


def community_story_picture_upload_location(self, filename='ci'):
    file_path = f'story/community_story/{str(self.community.name)}/{str(self.id)}-{str(self.user.username)}-{filename}.png'
    return file_path


class Story(models.Model):
    story_video = models.URLField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(null=False, blank=False)

    class Type(models.TextChoices):
        IMAGE = 0, _('Image')
        VIDEO = 1, _('Video')

    type = models.CharField(max_length=10, choices=Type.choices, null=False, blank=False)

    date_created = models.DateTimeField(verbose_name='date created',
                                        auto_now_add=True)  # auto_now_add save date only while creating an object
    date_updated = models.DateTimeField(verbose_name='date updated', auto_now=True)


class UserStory(Story):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_story_user')
    story_picture = models.ImageField(max_length=255, upload_to=user_story_picture_upload_location, null=True,
                                      blank=True)

    def __str__(self):
        return f'User Story: posted: {self.user.username}, {self.type}, {self.date_created}, {self.date_created}'


class GroupStory(Story):
    group = models.ForeignKey(GroupT, on_delete=models.CASCADE, related_name='group_story_group')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_story_user')
    story_picture = models.ImageField(max_length=255, upload_to=group_story_picture_upload_location, null=True,
                                      blank=True)

    def __str__(self):
        return f'Group Story: {self.group.group_title}, {self.type}, posted by: {self.user.username}, {self.date_created}'


class CommunityStory(Story):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_story_community')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_story_user')
    story_picture = models.ImageField(max_length=255, upload_to=community_story_picture_upload_location, null=True,
                                      blank=True)

    def __str__(self):
        return f'Community Story: {self.community.name}, {self.type}, posted: {self.user.username}, {self.date_created}'
