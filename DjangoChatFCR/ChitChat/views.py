from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Friend, ChatRoom
from django.contrib import messages
from .forms import ChatRoomForm

# Chat views
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)

def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {
        'room_name': room_name
    }
    return render(request, "chat/room.html", context)

# Friend management views
@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        try:
            friend = User.objects.get(username=friend_username)
            if friend != request.user:
                Friend.objects.create(user=request.user, friend=friend)
                Friend.objects.create(user=friend, friend=request.user)
                messages.success(request, f"You are now friends with {friend.username}")
            else:
                messages.error(request, "You cannot add yourself as a friend.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect('friends_list')

@login_required
def friends_list(request):
    friends = Friend.objects.filter(user=request.user)
    return render(request, 'friends_list.html', {'friends': friends})

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
    return render(request, 'create_chat_room.html', {'form': form})

@login_required
def list_chat_rooms(request):
    chat_rooms = request.user.chatrooms.all()
    return render(request, 'list_chat_rooms.html', {'chat_rooms': chat_rooms})

# Combined chat rooms and friends view
@login_required
def chat_rooms_and_friends(request):
    chat_rooms = request.user.chatrooms.all()
    friends = Friend.objects.filter(user=request.user)
    return render(request, 'chat_rooms_and_friends.html', {'chat_rooms': chat_rooms, 'friends': friends})

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    friends = Friend.objects.filter(user=request.user, is_accepted=True)
    chat_rooms = request.user.chatrooms.all()
    
    context = {
        'friends': friends,
        'chat_rooms': chat_rooms,
    }
    return render(request, "chat/chatPage.html", context)

