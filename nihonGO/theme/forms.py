# forms.py
from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class FlashcardForm(forms.ModelForm):
    PART_OF_SPEECH_CHOICES = [
        ('noun', 'Noun'),
        ('verb', 'Verb'),
        ('い adjective', 'い Adjective'),
        ('な adjective', 'な Adjective'),
        ('n/a', 'n/a'),
    ]
    
    part_of_speech = forms.ChoiceField(choices=PART_OF_SPEECH_CHOICES)

    class Meta:
        model = Card
        fields = ['question', 'answer', 'part_of_speech']