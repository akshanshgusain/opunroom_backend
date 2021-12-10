from django.contrib import admin

# Register your models here.
from community.models import Community


class CommunityAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined','id')


admin.site.register(Community, CommunityAdmin)


