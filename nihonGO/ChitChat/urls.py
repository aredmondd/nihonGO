from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home, name="home"),  # Home page after login
    path("auth/login/", LoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("chat/", views.chatPage, name="chat-page"),  # Chat page
    path("chat/<str:room_name>/", views.room, name='room'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('create_room/', views.create_chat_room, name='create_chat_room'),
    path('chat_rooms/', views.list_chat_rooms, name='list_chat_rooms'),
    path('chat_rooms_and_friends/', views.chat_rooms_and_friends, name='chat_rooms_and_friends'),
    path('pending_friend_requests/', views.pending_friend_requests, name='pending_friend_requests'),
    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('chats/', views.chat_list, name='chat_list'),  # Added this line
    path('chats/<int:friend_id>/', views.chat_room, name='chat_room'),  # Added this line
    path('chats/room/<int:room_id>/', views.chat_room_detail, name='chat_room_detail'),  # Added this line
]
