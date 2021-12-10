from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, OTP


class CustomsUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'phone_number', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('username', 'phone_number')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()

    # Fields inside Each Record/Row
    fieldsets = ()

    # Fields in the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2')
        }),
    )

    ordering = ('date_joined',)


admin.site.register(Account, CustomsUserAdmin)
admin.site.register(OTP)
