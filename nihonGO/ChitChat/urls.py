from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Authentication routes
    path("messages/", views.messages_view, name="messages"),  # Updated to match the new view name

    # Chat page routes
    path("chat/", views.chatPage, name="chat-page"),
    path("chat/<str:room_name>/", views.room, name="room"),

    # Friend-related routes
    path('add_friend/', views.add_friend, name='add_friend'),
    path('friends/', views.friends_list, name='friends'),

    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),

    # Private chat room routes
    path('private_chat/<int:friend_id>/', views.chatPage, name='private_chat_room'),
    path('create_room/', views.create_chat_room, name='create_chat_room'),
    path('chat_rooms/', views.list_chat_rooms, name='list_chat_rooms'),
]