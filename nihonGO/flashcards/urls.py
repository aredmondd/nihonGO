from django.urls import path
from . import views

urlpatterns = [
    path('create_deck/', views.create_deck, name='create_deck'),
    path('decks/', views.deck_list, name='deck_list'),
    path('add_flashcard/<int:deck_id>/', views.add_flashcard, name='add_flashcard'),
]
