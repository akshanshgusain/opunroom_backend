from django.contrib import admin

# Register your models here.
from friend.models import FriendList, FriendRequest


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['id', 'sender', 'receiver']
    list_display = ['id', 'sender', 'receiver']
    search_fields = ['sender__username', 'sender__phone_number', 'receiver__username', 'receiver__phone_number']
    readonly_fields = ('id', )

    class Meta:
        model = FriendRequest


admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
