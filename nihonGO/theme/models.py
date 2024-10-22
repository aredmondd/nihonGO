# models.py
from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    deck = models.ForeignKey('Deck', related_name='flashcards', on_delete=models.CASCADE)
    vocab_word = models.CharField(max_length=255)
    kana = models.CharField(max_length=255)
    english_translation = models.TextField()
    part_of_speech = models.CharField(max_length=50)
    example_sentence = models.TextField()
    example_sentence_kana = models.TextField()
    example_sentence_english = models.TextField()

    def __str__(self):
        return self.vocab_word  # Return the question as the string representation

# Model for Deck 
class Deck(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    card_count = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)  # Field to indicate if this is a default deck
    def __str__(self):
        return self.name
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        Deck.objects.create(user=instance, name='Japanese Basics', description='A deck of basic Japanese vocabulary and phrases.', is_default=True)