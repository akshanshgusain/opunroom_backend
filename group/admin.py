from django.contrib import admin

# Register your models here.
from django.contrib.admin import display

from accounts.models import Account
from group.models import GroupT


class GroupTAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'id', 'last_update')

    list_display = ('group_title', 'id', 'group_founder_username')

    @display(description='Group Founder')
    def group_founder_username(self, obj):
        return obj.group_founder.username

    filter_horizontal = ()
    list_filter = ()

    # Fields inside Each Record/Row
    fieldsets = ()


admin.site.register(GroupT, GroupTAdmin)
