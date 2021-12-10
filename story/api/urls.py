from django.urls import path

from story.api.views import api_index, create_story,feed

app_name = 'story'

urlpatterns = [
    path('', api_index, name='api_index'),
    path('create_story/', create_story, name='create_story'),
    path('feed/', feed, name='feed'),
]
