# forms.py
from django import forms
from .models import Deck, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['vocab_word', 'kana', 'english_translation', 'part_of_speech', 'example_sentence', 'example_sentence_kana', 'example_sentence_english']
