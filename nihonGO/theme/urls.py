from django.urls import path, include
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
    path('mydecks/', views.my_decks, name="my_decks"),
    path('add/', views.add_deck, name='add_deck'),
    path('study/<int:deck_id>/', views.study, name='study'),
    path('edit/<int:deck_id>/', views.edit_deck, name='edit_deck'),
    path('delete/<int:deck_id>/', views.delete_deck, name='delete_deck'),  
]