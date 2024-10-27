from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile

urlpatterns = [
    path('', views.home, name="home"),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('profile-page', views.profile_page, name="profile-page"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('profile/', profile, name='users-profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]