# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

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

class UserCardProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    last_reviewed = models.DateTimeField(default=timezone.now)
    next_review_date = models.DateTimeField(default=timezone.now)
    ease_factor = models.FloatField(default=2.5)  # Controls the learning interval
    interval = models.IntegerField(default=1)  # Days until the next review
    repetition_count = models.IntegerField(default=0)

    def update_progress(self, correct):
        if correct:
            self.repetition_count += 1
            self.ease_factor = max(1.3, self.ease_factor + 0.1)  # Increase ease factor slightly for correct answers
            self.interval = self.interval * self.ease_factor  # Increase interval based on ease factor
        else:
            self.repetition_count = 0
            self.ease_factor = max(1.3, self.ease_factor - 0.2)  # Decrease ease factor for incorrect answers
            self.interval = 1  # Reset interval on incorrect answer

        self.last_reviewed = timezone.now()
        self.next_review_date = timezone.now() + timedelta(days=int(self.interval))
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.card.vocab_word}"