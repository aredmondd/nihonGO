from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('forum/', views.forum, name="forum"),
    path('my-profile/', views.profile, name="my-profile"),
    path('profile-page/', views.profile_page, name="profile-page"),
    path('user-logout/', views.user_logout, name="user-logout"),
    path('profile/', views.profile, name='users-profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #this is not correct
    path('chat/', include('ChitChat.urls')),
]

# URL patterns specific to ChitChat app
chat_urlpatterns = [
    path("", views.chatPage, name="chat-page"),
    path("auth/login/", auth_views.LoginView.as_view(template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout-user"),
    path("<str:room_name>/", views.room, name='room'),
]

urlpatterns += chat_urlpatterns
