from rest_framework import serializers

from story.models import UserStory, GroupStory, CommunityStory


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = '__all__'


class GroupStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStory
        fields = '__all__'


class CommunityStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityStory
        fields = '__all__'
