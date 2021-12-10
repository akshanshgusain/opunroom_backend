from django.urls import path

from accounts import api
from accounts.api.views import api_view_home, get_otp, user_exit, check_username, log_in, register, get_communities, \
    search_user, search_user_profile, update_profile

app_name = 'accounts'

urlpatterns = [
    path('api_view/', api_view_home, name='api_home'),
    path('get_otp/', get_otp, name='example_func'),
    path('check_user/', user_exit, name='check_user'),
    path('check_username/', check_username, name='check_username'),
    path('login/', log_in, name='log_in'),
    path('register/', register, name='register'),
    path('update_profile/', update_profile, name='update_profile'),
    path('get_communities/', get_communities, name='get_communities'),
    path('search_user/', search_user, name='search_user'),
    path('search_user_profile/', search_user_profile, name='search_user_profile'),
]
