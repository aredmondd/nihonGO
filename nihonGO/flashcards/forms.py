# flashcards/forms.py
from django import forms
from .models import Deck, Flashcard

# Form for Deck model
class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']  # You can add more fields if necessary (e.g., description)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deck Name'}),
        }

# Form for Flashcard model
class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer', 'deck']  # You can include all relevant fields
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the answer'}),
            'deck': forms.Select(attrs={'class': 'form-control'}),
        }
