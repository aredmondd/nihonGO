from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Home page
    path("messages/", views.home, name="home"),

    # Authentication routes
    path("messages/auth/login/", LoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("messages/auth/logout/", LogoutView.as_view(), name="logout-user"),

    # Messages view
    path("messages/messages/", views.messages, name="messages"),

    # Chat page routes
    path("messages/chat/", views.chatPage, name="chat-page"),
    path("messages/chat/<str:room_name>/", views.room, name="room"),

    # Friend-related routes
    path('messages/add_friend/', views.add_friend, name='add_friend'),
    path('messages/friends_list/', views.friends_list, name='friends_list'),
    path('messages/pending_friend_requests/', views.pending_friend_requests, name='pending_friend_requests'),
    path('messages/accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('messages/reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('messages/remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),

    # Private chat room routes
    path('messages/private_chat/<int:friend_id>/', views.private_chat, name='private_chat_room'),
    path('messages/create_room/', views.create_room, name='create_chat_room'),
    path('messages/chat_rooms/', views.list_chat_rooms, name='list_chat_rooms'),
    path('messages/chat_rooms_and_friends/', views.chat_rooms_and_friends, name='chat_rooms_and_friends'),
]
