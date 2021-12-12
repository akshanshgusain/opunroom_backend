from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.api.serializers import AccountSerializer
from accounts.models import Account
from community.models import Community
from group.api.serializers import GroupTSerializer
from group.models import GroupT


@api_view(['POST'])
def get_groups(request):
    user_id = request.data.get('user_id')
    member = Account.objects.filter(id=user_id).first()
    if member is None:
        return Response({'status': False,
                         'message': 'User Does not Exist!',
                         'result': {}})
    else:
        group = GroupT.objects.filter(group_folks=member).all()
        group_serializer = GroupTSerializer(group, many=True)
        if group is None:
            return Response({'status': False,
                             'message': 'No Groups',
                             'result': group_serializer.data})

        return Response({'status': True,
                         'message': 'Success',
                         'result': group_serializer.data})


@api_view(['POST', ])
def get_community_members(request):
    admin_id = request.data.get('user_id')
    admin = Account.objects.filter(id=admin_id).first()
    if admin is None:
        return Response({'status': False,
                         'message': 'User Does not Exist!',
                         'result': {}})
    else:
        account_community = Community.objects.filter(group_folks=admin).first()
        if account_community is None:
            return Response({'status': False,
                             'message': 'User Does not Belong to Any Community',
                             'result': {}})
        else:
            members_of_same_community = account_community.group_folks.all()
            account_serializer = AccountSerializer(members_of_same_community, many=True)
            return Response({'status': True,
                             'message': 'Group members: ',
                             'result': account_serializer.data})


@api_view(['POST', ])
def get_group_members(request):
    group_id = request.data.get('group_id')
    try:
        group = GroupT.objects.get(id=group_id)
    except Exception as e:
        return Response({'status': False,
                         'message': 'Group Does Not Exist',
                         'result': {}})
    group_members = group.group_folks
    serialize = AccountSerializer(group_members, many=True)
    return Response({'status': True,
                     'message': 'Success',
                     'result': serialize.data})


@api_view(['POST'])
def create_group(request):
    admin_id = request.data.get('user_id')
    member_ids = list(filter(None, request.data.get('member_ids').split(',')))
    group_title = request.data.get('group_title')

    admin = Account.objects.filter(id=admin_id).first()
    if admin is None:
        return Response({'status': False,
                         'message': 'User Does not Exist!',
                         'result': {}})
    else:
        try:
            new_group = GroupT(group_founder=admin, group_title=group_title)
            new_group.save()
        except IntegrityError as e:
            return Response({'status': False,
                             'message': 'Group Title needs to be Unique',
                             'result': {}})

        members = Account.objects.filter(id__in=member_ids).all()
        for member in members:
            new_group.group_folks.add(member)
        new_group.group_folks.add(admin)
        group_t_serializer = GroupTSerializer(new_group)

        return Response({'status': True,
                         'message': 'Group Created',
                         'result': group_t_serializer.data})


@api_view(['POST'])
def update_group(request):
    group_id = request.data.get('group_id')
    member_ids = list(filter(None, request.data.get('member_ids').split(',')))
    group_title = request.data.get('group_title')

    group = GroupT.objects.filter(id=group_id).first()
    members = Account.objects.filter(id__in=member_ids).all()
    group.group_folks.clear()
    for member in members:
        group.group_folks.add(member)
    group.group_title = group_title
    group.save()
    group_serializer = GroupTSerializer(group)
    return Response({'status': True,
                     'message': 'Group Created',
                     'result': group_serializer.data})
