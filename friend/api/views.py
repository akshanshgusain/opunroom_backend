from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.api.serializers import AccountSerializer
from accounts.models import Account
from friend.api.serializers import FriendRequestSerializer
from friend.models import FriendRequest, FriendList


@api_view(['GET'])
def api_index(request):
    return Response('API - Friend Index')


@api_view(['POST'])
def send_friend_request(request):
    sender_id = request.data.get('sender_id')
    sender = Account.objects.get(id=sender_id)
    receiver_id = request.data.get('receiver_id')
    receiver = Account.objects.get(id=receiver_id)

    try:
        # Get any Friend requests (active and not-active)
        friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)

        # Find if any of them ae active
        try:
            for request in friend_requests:
                if request.is_active:
                    return Response({
                        'status': False,
                        'message': 'Friend Request Already sent!',
                        'result': {}
                    })
            # IF none are active, then create a new friend request
            friend_request = FriendRequest(sender=sender, receiver=receiver)
            friend_request.save()
            serializer = FriendRequestSerializer(friend_request)

            return Response({
                'status': True,
                'message': 'Friend Request sent!',
                'result': serializer.data
            })
        except Exception as e:
            raise e
    except Exception as e:
        # There are no Friend Request ever sent so create one.
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)

        return Response({
            'status': True,
            'message': 'Friend Request sent!',
            'result': serializer.data
        })


@api_view(['POST'])
def accept_friend_request(request):
    user_id = request.data.get('user_id')
    friend_request_id = request.data.get('friend_request_id')
    user = Account.objects.get(id=user_id)

    friend_request = FriendRequest.objects.get(id=friend_request_id)

    # Check if that is the correct request
    if user == friend_request.receiver:
        friend_request.accept()
        return Response({
            'status': True,
            'message': 'Friend Request Accepted',
            'result': {}
        })
    else:
        return Response({
            'status': False,
            'message': 'Something went wrong',
            'result': {}
        })


@api_view(['POST'])
def decline_friend_request(request):
    user_id = request.data.get('user_id')
    friend_request_id = request.data.get('friend_request_id')

    user = Account.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(id=friend_request_id)

    if user == friend_request.receiver:
        friend_request.decline()
        return Response({
            'status': True,
            'message': 'Friend Request Declined',
            'result': {}
        })
    else:
        return Response({
            'status': False,
            'message': 'Something went wrong',
            'result': {}
        })


@api_view(['POST'])
def cancel_friend_request(request):
    user_id = request.data.get('user_id')
    friend_request_id = request.data.get('friend_request_id')

    user = Account.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(id=friend_request_id)

    if user == friend_request.sender:
        friend_request.cancel()
        return Response({
            'status': True,
            'message': 'Friend Request Canceled',
            'result': {}
        })
    else:
        return Response({
            'status': False,
            'message': 'Something went wrong',
            'result': {}
        })


@api_view(['POST'])
def unfriend(request):
    remover_user_id = request.data.get('user_id')
    removee_user_id = request.data.get('friend_id')

    try:
        remover = Account.objects.get(id=remover_user_id)
        removee = Account.objects.get(id=removee_user_id)
        friend_list = FriendList.objects.get(user=remover)
        friend_list.unfriend(removee)
        return Response({
            'status': True,
            'message': 'Friend Unfriended',
            'result': {}
        })
    except Exception as e:
        return Response({
            'status': False,
            'message': 'Something went wrong',
            'result': {}
        })


@api_view(['POST'])
def get_all_friend_requests(request):
    user_id = request.data.get('user_id')
    user = Account.objects.get(id=user_id)

    friend_requests = FriendRequest.objects.filter(receiver=user).filter(is_active=True).all()
    friend_requests_serializer = FriendRequestSerializer(friend_requests, many=True)

    return Response({
        'status': True,
        'message': 'Success',
        'result': friend_requests_serializer.data
    })


@api_view(['POST'])
def get_all_friends(request):
    user_id = request.data.get('user_id')
    user = Account.objects.get(id=user_id)

    friends = FriendList.objects.all()
    friend_serializer = AccountSerializer(friends, many=True)

    return Response({
        'status': True,
        'message': 'Success',
        'result': friend_serializer.data
    })
