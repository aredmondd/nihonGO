# ChitChat/context_processors.py
from .models import Friend

def friend_count(request):
    if request.user.is_authenticated:
        num_friend_requests = Friend.objects.filter(friend=request.user, is_accepted=False).count()
        return {'num_friend_requests': num_friend_requests}
    return {'num_friend_requests': -1} 
