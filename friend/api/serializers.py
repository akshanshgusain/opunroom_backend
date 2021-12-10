from rest_framework import serializers

from accounts.api.serializers import AccountSerializer
from friend.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = AccountSerializer()
    receiver = AccountSerializer()

    class Meta:
        model = FriendRequest
        fields = '__all__'
