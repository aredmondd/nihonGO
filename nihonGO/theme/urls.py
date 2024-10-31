from django.urls import path, include
from . import views
from .views import profile
from django.contrib.auth import views as auth_views
from .views import messages


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('forum/', views.forum, name="forum"),
    path('my-profile/', views.profile, name="my-profile"),
    #path('messages/', views.messages, name="messages"),
    path('mydecks/', views.my_decks, name="my_decks"),
    path('add/', views.add_deck, name='add_deck'),
    path('study/<int:deck_id>/', views.study, name='study'),
    path('profile-page', views.profile_page, name="profile-page"),
    path('user-logout', views.user_logout, name="user-logout"),
    path('profile/', profile, name='users-profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit/<int:deck_id>/', views.edit_deck, name='edit_deck'),
    path('delete/<int:deck_id>/', views.delete_deck, name='delete_deck'),  
    #path('chat/<str:recipient_username>/', views.chat_view, name='chat'),
    path('chat/', views.chat_view, name='chat'), 
]