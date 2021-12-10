from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from story.models import UserStory, GroupStory, CommunityStory


class CustomUserStory(UserAdmin):
    list_display = ('type', 'duration', 'date_created')
    search_fields = ('type',)
    readonly_fields = ('id', 'date_created', 'date_updated')

    # @display(description='Created By')
    # def user_username_re(self, obj):
    #     print(obj)
    #     return obj.user.username

    filter_horizontal = ()
    list_filter = ()

    # Fields inside Each Record/Row
    fieldsets = ()

    # Fields in the user creation form
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('user', 'story_picture', 'story_video', 'type', 'duration')
    #     }),
    # )

    ordering = ('date_created',)


admin.site.register(UserStory)
admin.site.register(GroupStory)
admin.site.register(CommunityStory)
