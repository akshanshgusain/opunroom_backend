from django.urls import path

from friend.views import index

urlpatterns = [
    path('', index, name='index'),
]