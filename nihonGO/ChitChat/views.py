from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Friend, ChatRoom, PrivateChat
from django.contrib import messages
from .forms import ChatRoomForm
from .models import PrivateChat, User
from django.contrib.auth.views import LoginView

# Chat views
@login_required
def chatPage(request, *args, **kwargs):
    context = {}
    return render(request, "chat/chatPage.html", context)

@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        'room_name': room_name,
        'username': request.user.username
    })

@login_required
def chat_room(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    # Create or get an existing chat room
    chat_room, created = ChatRoom.objects.get_or_create(name=f"{request.user.username}_{friend.username}")
    
    # Add the user and friend to the chat room
    if created:
        chat_room.users.add(request.user, friend)
    else:
        # Ensure both users are part of the chat room if not already added
        if request.user not in chat_room.users.all():
            chat_room.users.add(request.user)
        if friend not in chat_room.users.all():
            chat_room.users.add(friend)

    return redirect('chat_room_detail', room_id=chat_room.id)

@login_required
def chat_room_detail(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    return render(request, 'chat/chat_room_detail.html', {'chat_room': chat_room})

# Friend management views
@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        try:
            friend = User.objects.get(username=friend_username)
            if friend != request.user:
                # Check if a friend request already exists
                existing_request = Friend.objects.filter(user=request.user, friend=friend, is_accepted=False).exists()
                if not existing_request:
                    Friend.objects.create(user=request.user, friend=friend)
                    messages.success(request, f"Friend request sent to {friend.username}")
                else:
                    messages.warning(request, f"Friend request already sent to {friend.username}")
            else:
                messages.error(request, "You cannot add yourself as a friend.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    friends = Friend.objects.filter(user=request.user, is_accepted=True)
    friend_requests_received = Friend.objects.filter(friend=request.user, is_accepted=False)
    num_friend_requests = friend_requests_received.count()
    return render(request, 'chat/friends.html', {
        'friends': friends,
        'friend_requests_received': friend_requests_received,
        'num_friend_requests': num_friend_requests
    })

@login_required
def friends_list(request):
    friends = Friend.objects.filter(user=request.user, is_accepted=True)
    friend_requests_received = Friend.objects.filter(friend=request.user, is_accepted=False)
    num_friend_requests = friend_requests_received.count()
    return render(request, 'chat/friends.html', {
        'friends': friends,
        'friend_requests_received': friend_requests_received,
        'num_friend_requests': num_friend_requests
    })


@login_required
def accept_friend_request(request, friend_request_id):
    try:
        friend_request = Friend.objects.get(id=friend_request_id, friend=request.user)
        friend_request.is_accepted = True
        friend_request.save()
        Friend.objects.create(user=friend_request.friend, friend=friend_request.user, is_accepted=True)
        messages.success(request, f"You are now friends with {friend_request.user.username}")
    except Friend.DoesNotExist:
        messages.error(request, "Friend request not found.")
    return redirect('friends')

@login_required
def reject_friend_request(request, friend_request_id):
    try:
        friend_request = Friend.objects.get(id=friend_request_id, friend=request.user)
        friend_request.delete()
        messages.success(request, f"Friend request from {friend_request.user.username} has been rejected")
    except Friend.DoesNotExist:
        messages.error(request, "Friend request not found.")
    return redirect('friends')

@login_required
def remove_friend(request, friend_id):
    try:
        friend = Friend.objects.get(id=friend_id, user=request.user)
        reciprocal_friend = Friend.objects.filter(user=friend.friend, friend=request.user).first()
        if reciprocal_friend:
            reciprocal_friend.delete()
        friend.delete()
        messages.success(request, f"Unfriended {friend.friend.username}")
    except Friend.DoesNotExist:
        messages.error(request, "Friend not found.")
    return redirect('friends')

# Chat room management views
@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.save()
            chat_room.members.add(request.user)
            return redirect('list_chat_rooms')
    else:
        form = ChatRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form})

@login_required
def list_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    user_chat_rooms = request.user.chatrooms.all()
    return render(request, 'chat/list_chat_rooms.html', {
        'chat_rooms': chat_rooms,
        'user_chat_rooms': user_chat_rooms,
    })

@login_required
def join_chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    chat_room.members.add(request.user)
    messages.success(request, f"You have joined the chat room {chat_room.name}.")
    return redirect('list_chat_rooms')

@login_required
def leave_chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    chat_room.members.remove(request.user)
    messages.success(request, f"You have left the chat room {chat_room.name}.")
    return redirect('list_chat_rooms')

@login_required
def private_chat(request, friend_id):
    user1 = request.user
    user2 = get_object_or_404(User, id=friend_id)
    private_chat, created = PrivateChat.objects.get_or_create(user1=user1, user2=user2)
    
    if not created:
        private_chat = PrivateChat.objects.filter(user1=user1, user2=user2).first()
        if not private_chat:
            private_chat = PrivateChat.objects.get(user1=user2, user2=user1)

    context = {
        'private_chat': private_chat,
        'friend': user2,
    }
    return render(request, 'chat/private_chat.html', context)

def messages_view(request): 
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/home.html', {
        'chat_rooms' : chat_rooms,
    })

@login_required
def friends(request):
    friends = Friend.objects.filter(user=request.user, is_accepted=True)
    return render(request, 'chat/friends.html', {'friends': friends,})