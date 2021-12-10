from django.conf import settings
from django.db import models


# Create your models here.


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return f'{self.user.username}'

    ''' Core Functionality '''

    def add_friend(self, account):
        # Add a new friend
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        # Un-Friend
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    ''' Helper Functions '''

    def unfriend(self, removee):
        # Self is the remover who is removing the removee from his friend list
        # Initiate the action on unfriending someone.
        remover = self  # person terminating the friendship

        # Remove friend from remover's friends list
        remover.remove_friend(removee)

        # Remove friend from removee's friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    '''
    A friend request consist of two main parts:
    1. Sender:
        - Person sending/initiating the friend request
    2. Receiver:
        - Person receiving the friend request
    '''
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    ''' Helper Functions '''

    def accept(self):
        # Accept a friend request
        # Update both Sender's and Receiver's friend list
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        # decline a friend request
        # It is declined by setting the is_active field to false
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        It is cancelled by setting the is_active field to False.
        This is only different with respect to declining through the notification that is generated.
        """
        self.is_active = False
        self.save()
