import os
import traceback

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.api.serializers import AccountSerializer, CommunitySerializer
from accounts.models import Account
from community.models import Community
from friend.models import FriendList
from group.api.serializers import GroupT2Serializer
from group.models import GroupT
from story.api.serializers import UserStorySerializer, GroupStorySerializer, CommunityStorySerializer
from story.models import StoryType, UserStory, GroupStory, CommunityStory


@api_view(['GET'])
def api_index(request):
    return Response('Story Api index')


@api_view(['POST'])
def create_story(request):
    if request.data.get('user_id') and request.data.get('duration') and request.data.get('story_type'):
        story_poster_id = request.data.get('user_id')
        duration = request.data.get('duration')
        story_type = int(request.data.get('story_type'))
        story_poster = Account.objects.get(id=story_poster_id)
    else:
        return Response({'status': False,
                         'message': f'Field Missing',
                         'result': {}})

    if story_type == StoryType.IMAGE_STORY.value:
        # Get Image
        story_picture = request.FILES['story_picture']
        # Add Story to Poster's Story
        if request.data.get('self_id'):
            user_story = UserStory(user=story_poster,
                                   duration=duration,
                                   type=story_type,
                                   story_picture=story_picture,
                                   story_video=None)

            try:
                user_story.save()
                story_picture = user_story.story_picture
            except RuntimeError as er:
                print(er)
                print(traceback.format_exc())
            except Exception as e:
                return Response({'status': False,
                                 'message': f'Image-userStory: {e}',
                                 'result': {}})
        # Add Story to Selected Groups
        if request.data.get('group_ids'):
            group_ids = list(filter(None, request.data.get('group_ids').split(',')))
            for group_id in group_ids:
                group = GroupT.objects.get(id=group_id)
                group_story = GroupStory(
                    group=group,
                    user=story_poster,
                    duration=duration,
                    type=story_type,
                    story_picture=story_picture,
                    story_video=None,
                )
                try:
                    group_story.save()
                    story_picture = group_story.story_picture
                except RuntimeError as er:
                    print(er)
                    print(traceback.format_exc())
                except Exception as e:
                    return Response({'status': False,
                                     'message': f'Image-groupStory: {e}, {type(e)}, ids: {group_ids}',
                                     'result': {}})

        # Add Story to selected Communities
        if request.data.get('community_ids'):
            community_ids = list(filter(None, request.data.get('community_ids').split(',')))
            for community_id in community_ids:
                community = Community.objects.get(id=community_id)
                community_story = CommunityStory(
                    community=community,
                    user=story_poster,
                    duration=duration,
                    type=story_type,
                    story_picture=story_picture,
                    story_video=None
                )
                try:
                    community_story.save()
                    story_picture = community_story.story_picture
                except RuntimeError as er:
                    print(er)
                except Exception as e:
                    print(e)
                    return Response({'status': False,
                                     'message': f'Image-communityStory: {e}, ids: {community_ids}',
                                     'result': {}})
        return Response({'status': True,
                         'message': 'Success',
                         'result': {}})

    elif story_type == StoryType.VIDEO_STORY.value:
        story_video = request.data.get('story_video')
        # Get Video URL

        if request.data.get('self_id'):
            user_story = UserStory(user=story_poster,
                                   duration=duration,
                                   type=story_type,
                                   story_picture=None,
                                   story_video=story_video)
            user_story.save()
        if request.data.get('group_ids'):
            group_ids = list(filter(None, request.data.get('group_ids').split(',')))
            for group_id in group_ids:
                group = GroupT.objects.get(id=group_id)
                group_story = GroupStory(
                    group=group,
                    user=story_poster,
                    duration=duration,
                    type=story_type,
                    story_picture=None,
                    story_video=story_video,
                )
                group_story.save()
        if request.data.get('community_ids'):
            community_ids = list(filter(None, request.data.get('community_ids').split(',')))
            for community_id in community_ids:
                community = Community.objects.get(id=community_id)
                community_story = CommunityStory(
                    community=community,
                    user=story_poster,
                    duration=duration,
                    type=story_type,
                    story_picture=None,
                    story_video=story_video
                )
                community_story.save()
            return Response({'status': True,
                             'message': 'Success',
                             'result': {}})
    else:
        return Response({'status': False,
                         'message': 'Invalid Type',
                         'result': {}})


@api_view(['POST'])
def feed(request):
    user_id = request.data.get('user_id')
    user = Account.objects.get(id=user_id)

    # Friends
    all_friends = FriendList.objects.get(user=user).friends.all()
    # friends_serialized = AccountSerializer(all_friends, many=True)

    """get story_picture of all the friends"""
    friends = []
    for friend in all_friends:
        friend_serialized = AccountSerializer(friend)
        friend_dict = friend_serialized.data
        stories = UserStory.objects.filter(user=friend).all()
        story_serializer = UserStorySerializer(stories, many=True)
        friend_dict['story_picture'] = story_serializer.data
        friends.append(friend_dict)

    """get story_picture of self"""
    user_dict = AccountSerializer(user).data
    user_stories = UserStory.objects.filter(user=user).all()
    user_stories_serialized = UserStorySerializer(user_stories, many=True)
    user_dict['story_pictures'] = user_stories_serialized.data

    """get story_pictures of groups"""

    # Get all Groups
    all_groups = []
    _all_groups = GroupT.objects.all()
    for _group in _all_groups:
        members = _group.group_folks.all()
        if user in members:
            all_groups.append(_group)

    groups = []
    # Get stories for each group
    for group in all_groups:
        group_serialized = GroupT2Serializer(group).data
        stories = GroupStory.objects.filter(group=group).all()
        stories_serialized = GroupStorySerializer(stories, many=True)
        group_serialized['story_pictures'] = stories_serialized.data
        groups.append(group_serialized)

    """ Get story_pictures of community """

    # Get all Communities
    all_communities = []
    _all_communities = Community.objects.all()
    for _community in _all_communities:
        members = _community.community_folks.all()
        if user in members:
            all_communities.append(_community)

    communities = []
    # Get stories for each community
    for community in all_communities:
        community_serialized = CommunitySerializer(community).data
        stories = CommunityStory.objects.filter(community=community).all()
        stories_serialized = CommunityStorySerializer(stories, many=True)
        community_serialized['story_picture'] = stories_serialized.data
        communities.append(community_serialized)

    return Response({'status': True,
                     'message': 'Success',
                     'result': {
                         'friends': friends,
                         'self': user_dict,
                         'groups': groups,
                         'user_story': user_stories_serialized.data,
                         'communities': communities
                     }})
