from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.chatPage, name="chat-page"),
    path("auth/login/", LoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path("<str:room_name>/", views.room, name='room'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('create_room/', views.create_chat_room, name='create_chat_room'),
    path('chat_rooms/', views.list_chat_rooms, name='list_chat_rooms'),
    path('chat_rooms_and_friends/', views.chat_rooms_and_friends, name='chat_rooms_and_friends'),  # Added this line
]
