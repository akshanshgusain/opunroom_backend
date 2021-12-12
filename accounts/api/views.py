import string
import random

from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import helper
from accounts.api.serializers import AccountSerializer, CommunitySerializer
from accounts.models import Account
from community.models import Community
from friend.friend_request_status import FriendRequestStatus
from friend.helper import get_friend_request_or_false
from friend.models import FriendList
from group.api.serializers import GroupT2Serializer
from group.models import GroupT


@api_view(['GET'])
def api_view_home(request):
    return Response({'message': 'Aditya Chauhan', 'sutom message': ''})


@api_view(['GET'])
def example_func(request):
    return Response({'message': 'Mansi Chauhan', 'sutom message': ''})


@api_view(['POST'])
def get_otp(request):
    phone_number = request.data.get('phone_number')
    if phone_number is None:
        dict_result = {"status": False,
                       "message": "No mobile number entered",
                       "result": {"session_id": "Not Generated"}}

        return Response(dict_result)

    elif len(phone_number) < 10:
        dict_result = {"status": False,
                       "message": "Invalid phone numbers",
                       "result": {"session_id": "Not Generated"}}
        return Response(dict_result)
    else:
        response = helper.send_otp(phone_number)
        if response['Status'] == 'Success':
            session_id = response['Details']
            dict_result = {"status": True,
                           "message": "success",
                           "result": {"session_id": session_id}}
            return Response(dict_result)


# Base on Phone Number check if this user exist in the system or not.
@api_view(['POST'])
def user_exit(request):
    phone_number = request.data.get('phone_number')
    query = Account.objects.filter(phone_number=phone_number).first()

    if query is None:
        return Response({"id": -1,
                         "password": "",
                         "username": "",
                         "date_joined": "",
                         "last_login": "",
                         "is_admin": False,
                         "is_active": False,
                         "is_staff": False,
                         "is_superuser": False,
                         "f_name": "First Name",
                         "l_name": "Last Name",
                         "phone_number": "",
                         "email": "",
                         "profile_image": "/media/opundoor/img/default_profile_image.png",
                         "cover_image": "/media/opundoor/img/default_cover_image.png",
                         "privacy": "1"})
    else:
        account_serializer = AccountSerializer(query)
        return Response(account_serializer.data)


@api_view(['POST'])
def check_username(request):
    username = request.data.get('username')
    username_query = Account.objects.filter(username=username.lower()).first()
    if username_query is None:
        return Response({'status': True, 'message': 'username is valid', 'result': {}})
    else:
        return Response({'status': False, 'message': 'username is not valid', 'result': {}})


@api_view(['POST'])
def log_in(request):
    phone_number = request.data.get('phone_number')
    otp = request.data.get('otp')
    session_id = request.data.get('session_id')

    response = helper.verify_otp(session_id, otp)
    if response['Status'] == 'Error':
        dict_result = {"status": False,
                       "message": "Invalid Otp",
                       "result": {
                           "id": -1,
                           "password": "",
                           "username": "",
                           "date_joined": "",
                           "last_login": "",
                           "is_admin": False,
                           "is_active": False,
                           "is_staff": False,
                           "is_superuser": False,
                           "f_name": "First Name",
                           "l_name": "Last Name",
                           "phone_number": "",
                           "email": "",
                           "profile_image": "/media/opundoor/img/default_profile_image.png",
                           "cover_image": "/media/opundoor/img/default_cover_image.png",
                           "privacy": "1"
                       }}
        return Response(dict_result)
    else:
        phone_number = request.data.get('phone_number')
        query = Account.objects.filter(phone_number=phone_number).first()
        account_serializer = AccountSerializer(query)
        dict_result = {"status": True,
                       "message": "Success",
                       "result": account_serializer.data}
        return Response(dict_result)


@api_view(['POST'])
def register(request):
    phone_number = request.data.get('phone_number')
    username = request.data.get('username').lower()
    password = helper.password_generator()
    otp = request.data.get('otp')
    session_id = request.data.get('session_id')

    print(f'{password} generated password')

    user = Account.objects.filter(username__exact=username)
    response = helper.verify_otp(session_id, otp)
    if response['Status'] == 'Error':
        dict_result = {"status": False,
                       "message": "Invalid Otp",
                       "result": {
                           "id": -1,
                           "password": "",
                           "username": "",
                           "date_joined": "",
                           "last_login": "",
                           "is_admin": False,
                           "is_active": False,
                           "is_staff": False,
                           "is_superuser": False,
                           "f_name": "First Name",
                           "l_name": "Last Name",
                           "phone_number": "",
                           "email": "",
                           "profile_image": "/media/opundoor/img/default_profile_image.png",
                           "cover_image": "/media/opundoor/img/default_cover_image.png",
                           "privacy": "1"
                       }}
        return Response(dict_result)

    elif user.exists():
        return Response({
            'status': False,
            'message': 'User Already Exist',
            'result': {
                "id": -1,
                "password": "",
                "username": "",
                "date_joined": "",
                "last_login": "",
                "is_admin": False,
                "is_active": False,
                "is_staff": False,
                "is_superuser": False,
                "f_name": "First Name",
                "l_name": "Last Name",
                "phone_number": "",
                "email": "",
                "profile_image": "/media/opundoor/img/default_profile_image.png",
                "cover_image": "/media/opundoor/img/default_cover_image.png",
                "privacy": "1"
            }
        })
    else:
        try:
            account = Account(username=username, phone_number=phone_number)
            account.set_password(password)
            account.save()
            account_serializer = AccountSerializer(account)
            return Response({
                'status': True,
                'message': 'Success, Registered.',
                'result': account_serializer.data
            })

        except Exception as e:
            return Response({
                'status': False,
                'message': f'{e}',
                'result': {
                    "id": -1,
                    "password": "",
                    "username": "",
                    "date_joined": "",
                    "last_login": "",
                    "is_admin": False,
                    "is_active": False,
                    "is_staff": False,
                    "is_superuser": False,
                    "f_name": "First Name",
                    "l_name": "Last Name",
                    "phone_number": "",
                    "email": "",
                    "profile_image": "/media/opundoor/img/default_profile_image.png",
                    "cover_image": "/media/opundoor/img/default_cover_image.png",
                    "privacy": "1"
                }}
            )


@api_view(['POST'])
def update_profile(request):
    print(request)
    user_name = request.data.get('username')
    user = Account.objects.get(username=user_name)

    try:
        profile_image = request.FILES['profile_image']
        user.profile_image = profile_image
    except MultiValueDictKeyError as e:
        print(f'{e}. No Profile Picture')

    try:
        cover_image = request.FILES['cover_image']
        user.cover_image = cover_image
    except MultiValueDictKeyError as e:
        print(f'{e}. No Cover Picture')

    if request.data.get('f_name'):
        user.f_name = request.data.get('f_name')
    if request.data.get('l_name'):
        user.l_name = request.data.get('l_name')
    if request.data.get('privacy'):
        user.privacy = request.data.get('privacy')
    user.save()
    user_serialized = AccountSerializer(user)

    return Response({'status': True,
                     'message': 'Profile Updated',
                     'result': user_serialized.data})


@api_view(['GET', ])
def get_communities(request):
    communities = Community.objects.all()
    print(communities)
    communities_serializer = CommunitySerializer(communities, many=True)
    # if communities_serializer.is_valid():
    return Response({'status': True,
                     'message': 'Success',
                     'result': communities_serializer.data})
    # else:
    #     return Response({'': ''})


@api_view(['POST'])
def search_user(request):
    user_id = request.data.get('user_id')
    keyword = request.data.get('search_keyword')
    user = Account.objects.filter(id=user_id).first()

    if len(keyword) > 0:
        search_result = Account.objects.filter(
            Q(username__icontains=keyword) | Q(phone_number__contains=keyword)).distinct().exclude(id=user_id)

        print(search_result)
        serializer = AccountSerializer(search_result, many=True)
        return Response({'status': True,
                         'message': 'Success',
                         'result': serializer.data})
    else:
        return Response({'status': False,
                         'message': 'No Keyword!',
                         'result': []})


@api_view(['POST'])
def search_user_profile(request):
    user_id = request.data.get('user_id')
    friend_id = request.data.get('friend_id')

    user = Account.objects.get(id=user_id)
    friend = Account.objects.get(id=friend_id)
    account_serializer = AccountSerializer(friend)
    group = GroupT.objects.filter(group_folks=friend).first()
    group_serializer = GroupT2Serializer(group)

    # Friend State Logic

    # 1. You are looking at your own profile: i.e., user_id = friend_id
    if user_id == friend_id:
        return Response({'status': False,
                         'message': 'Pointing at the same profile!!',
                         'result': {}})

    # 2. You are not looking at your own profile
    try:
        friend_list = FriendList.objects.get(user=friend)  # Friend list of friend(Profile we are looking at)
    except FriendList.DoesNotExist as e:
        # No Friend List is found , create one
        friend_list = FriendList(user=friend)
        friend_list.save()
    friends = friend_list.friends.all()

    friends_serializer = AccountSerializer(friends, many=True)

    # 2.1. Are we friends?
    is_friend = True
    is_self = False
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    pending_friend_request_id = None

    if friends.filter(id=user_id):
        # 2.2. YES
        is_friend = True
    else:
        # 2.2. NO
        is_friend = False

        # 2.2.1. THEY Sent a friend request to you
        # FriendRequestStatus.THEM_SENT_TO_YOU
        if get_friend_request_or_false(sender=friend, receiver=user):
            request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
            pending_friend_request_id = get_friend_request_or_false(sender=friend, receiver=user).id

        # 2.2.2. YOU Sent a friend request to them
        # FriendRequestStatus.YOU_SENT_TO_THEM
        elif get_friend_request_or_false(sender=user, receiver=friend):
            request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            pending_friend_request_id = get_friend_request_or_false(sender=user, receiver=friend).id

        # 2.2.3. NO friend request have been sent
        # FriendRequestStatus.NO_REQUEST_SENT
        else:
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

    return Response({'status': True,
                     'message': 'Success',
                     'result': {'user': account_serializer.data,
                                'user_friends': friends_serializer.data,
                                'is_friend': is_friend,
                                'friend_request_status': request_sent,
                                'pending_friend_request_id': pending_friend_request_id}})
