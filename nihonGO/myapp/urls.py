from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('profile-page', views.profile_page, name="profile-page"),

    path('user-logout', views.user_logout, name="user-logout"),

    
]