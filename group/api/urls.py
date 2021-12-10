from django.urls import path

from group.api.views import get_groups, create_group, get_community_members, update_group, get_group_members

app_name = 'group'

urlpatterns = [
    path('get_groups/', get_groups, name='get_groups'),
    path('create_group/', create_group, name='create_group'),
    path('get_community_members/', get_community_members, name='get_community_members'),
    path('create_group/', create_group, name='create_group'),
    path('update_group/', update_group, name='update_group'),
    path('get_group_members/', get_group_members, name='get_group_members'),
]