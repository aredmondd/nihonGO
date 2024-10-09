from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('forum/', views.forum, name="forum"),
    path('my-profile/', views.profile, name="my-profile"),
    path('messages/', views.messages, name="messages"),
    path('decks/', views.decks, name="decks"),
]