from django.urls import path
from . import views
from .views import profile, ChangePasswordView

urlpatterns = [
    path('', views.home, name="home"),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('profile-page', views.profile_page, name="profile-page"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('profile/', profile, name='users-profile'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

    
]