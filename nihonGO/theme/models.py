# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
# Model for Deck 
class Deck(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    card_count = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)  # Field to indicate if this is a default deck
    description = models.TextField(blank=True)  # Add this line for description

    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    vocab_word = models.CharField(max_length=100)
    kana = models.CharField(max_length=100)
    english_translation = models.CharField(max_length=255, blank=True, null=True)
    part_of_speech = models.CharField(max_length=100, blank=True, null=True)
    example_sentence = models.TextField(blank=True, null=True)
    example_sentence_kana = models.TextField(blank=True, null=True)
    example_sentence_english = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.vocab_word  # Return the question as the string representation



    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_default_deck(sender, instance, created, **kwargs):
    if created:
        Deck.objects.create(user=instance, name='Japanese Basics', description='A deck of basic Japanese vocabulary and phrases.', is_default=True)

#-Profile class
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="theme_profile")

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

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
    
#MESSAGES - Alex
from django.db import models
from django.contrib.auth.models import User
class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat {self.id} between {", ".join([user.username for user in self.users.all()])}'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.recipient}: {self.content}'
    

#FORUM MODELS
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} to {self.post.title}"

