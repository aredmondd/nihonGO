# flashcards/models.py
from django.db import models
from django.contrib.auth.models import User

#Deck class
class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#flashcard class 
class Flashcard(models.Model):
    #this links each flashcard to the deck
    deck = models.ForeignKey(Deck, related_name="flashcards", on_delete=models.CASCADE)
    
    front_text = models.CharField(max_length=255)
    back_text = models.CharField(max_length=255)
    review_date = models.DateTimeField(null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.front_text
