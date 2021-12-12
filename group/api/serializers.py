from rest_framework import serializers

from accounts.api.serializers import AccountSerializer
from group.models import GroupT


class GroupTSerializer(serializers.ModelSerializer):
    group_folks = AccountSerializer(many=True)  # Group Folks will be a List of Account Type
    group_founder = AccountSerializer()

    class Meta:
        model = GroupT
        # fields = ('id', 'group_title', 'date_created', 'last_update', 'group_founder', 'group_folks')
        fields = '__all__'


class GroupT2Serializer(serializers.ModelSerializer):
    group_founder = AccountSerializer()

    class Meta:
        model = GroupT
        # fields = ('id', 'group_title', 'date_created', 'last_update', 'group_founder', 'group_folks')
        fields = '__all__'
