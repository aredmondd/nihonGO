# models.py
from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    deck = models.ForeignKey('Deck', related_name='flashcards', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question  # Return the question as the string representation

# Model for Deck 
class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    card_count = models.IntegerField(default=0)
    # Optional: Add a field to distinguish between deck types if needed
    type = models.CharField(max_length=50, choices=[('flashcards', 'Flashcards'), ('theme', 'Theme')], default='flashcards')

    def __str__(self):
        return self.name