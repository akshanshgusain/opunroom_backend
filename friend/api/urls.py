from django.urls import path

from friend.api.views import api_index, send_friend_request, accept_friend_request, unfriend, decline_friend_request, \
    cancel_friend_request, get_all_friend_requests, get_all_friends

app_name = 'friend'
urlpatterns = [
    path('', api_index, name='api_index'),
    path('send_friend_request/', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/', decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/', cancel_friend_request, name='cancel_friend_request'),
    path('unfriend/', unfriend, name='unfriend'),
    path('get_all_friend_requests/', get_all_friend_requests, name='get_all_friend_requests'),
    path('get_all_friends/', get_all_friends, name='get_all_friends'),
]
