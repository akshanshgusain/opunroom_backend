from rest_framework import serializers

from accounts.api.serializers import AccountSerializer
from story.models import UserStory, GroupStory, CommunityStory


class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = '__all__'


class GroupStorySerializer(serializers.ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = GroupStory
        fields = '__all__'


class CommunityStorySerializer(serializers.ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = CommunityStory
        fields = '__all__'
