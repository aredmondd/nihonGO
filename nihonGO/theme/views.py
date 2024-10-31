from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import Deck, Card

# Create your views here.
def index (request):
    return render(request, 'index.html')

def login (request):
    return render(request, 'login.html')

def register (request):
    return render(request, 'register.html')

def about (request):
    return render(request, 'about.html')

def dashboard (request):
    return render(request, 'dashboard.html')

def forum (request):
    return render(request, 'forum.html')

def profile (request):
    return render(request, 'my-profile.html')

def messages (request):
    return render(request, 'messages.html')


from django.conf import settings
import json
from .models import Deck
from .forms import DeckForm, FlashcardForm

#Use BASE_DIR to construct the relative path
file_path = f"{settings.BASE_DIR}/theme/templates/flashcards/japanesebasics.json"

#Open Japanese Basics
with open(file_path, 'r') as file:
    japaneseDict = json.load(file)


def my_decks(request):
    if not request.user.is_authenticated:
        # For non-authenticated users, show a default "Japanese Basics" deck.
        decks = [
            {'id': 1, 'name': 'Japanese Basics', 'cards': load_japanese_dict()},
            {'id': 2, 'name': 'Hiragana', 'cards': load_hiragana_dict},  # No cards
            {'id': 3, 'name': 'Katakana', 'cards': load_katakana_dict},  # No cards
        ]
    else:
        # Check if the default deck exists for authenticated users; if not, create it.
        user = request.user
        if not Deck.objects.filter(user=user, is_default=True).exists():
            create_default_deck(user)  # Create the deck for the user.
        
        # Fetch the user's decks including the default deck
        decks = Deck.objects.filter(user=user)
    
    return render(request, 'flashcards/mydecks.html', {'decks': decks})


def add_deck(request):
    if request.method == "POST":
        deck_form = DeckForm(request.POST)
        flashcard_forms = [FlashcardForm(request.POST) for _ in range(int(request.POST.get('num_cards', 0)))]

        if deck_form.is_valid() and all(f.is_valid() for f in flashcard_forms):
            new_deck = deck_form.save(commit=False)
            new_deck.user = request.user  # Associate deck with user
            new_deck.save()

            for flashcard_form in flashcard_forms:
                flashcard = flashcard_form.save(commit=False)
                flashcard.deck = new_deck  # Associate flashcard with the new deck
                flashcard.save()

                # Create UserCardProgress for each flashcard
                UserCardProgress.objects.create(
                    user=request.user,
                    card=flashcard,
                    last_reviewed=timezone.now(),
                    next_review_date=timezone.now(),
                    ease_factor=2.5,  # Initial values for spaced repetition
                    interval=1,
                    repetition_count=0,
                )

            return redirect('my_decks')
    else:
        deck_form = DeckForm()
        flashcard_forms = [FlashcardForm() for _ in range(3)]

    return render(request, 'flashcards/add_deck.html', {
        'deck_form': deck_form,
        'flashcard_forms': flashcard_forms,
    })

from .models import Card, Deck
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Deck, Card, UserCardProgress


# views.py

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Deck, Card
from datetime import timedelta


def study(request, deck_id):
    # Get the deck object
    deck = get_object_or_404(Deck, id=deck_id)
    
    # Allow all users to access the "Japanese Basics" deck without login
    if deck.is_default and deck.name == "Japanese Basics":
        # If the user is not logged in, do not apply spaced repetition
        if not request.user.is_authenticated:
            # Return all flashcards in the deck without filtering for spaced repetition
            context = {
                'deck': deck,
                'flashcards': deck.flashcards.all()
            }
            return render(request, 'flashcards/study.html', context)
    
    # If the user is logged in, apply spaced repetition logic for all decks
    elif request.user.is_authenticated:
        # Ensure user is authorized to access the deck (either it’s default or belongs to them)
        if not deck.is_default and deck.user != request.user:
            return redirect('login')  # Redirect if unauthorized access

        # Apply spaced repetition: show only flashcards that are due for review
        current_time = timezone.now()
        due_flashcards = deck.flashcards.filter(next_review_date__lte=current_time)
        
        context = {
            'deck': deck,
            'flashcards': due_flashcards
        }
        return render(request, 'flashcards/study.html', context)

    # If an anonymous user tries to access a non-default deck, redirect to login
    return redirect('login')


import os
import json
from django.conf import settings

def load_japanese_dict():
    file_path = os.path.join(settings.BASE_DIR, 'theme', 'templates', 'flashcards', 'japanesebasics.json')
    with open(file_path, 'r') as json_file:
        japanese_dict = json.load(json_file)
    return japanese_dict

def load_hiragana_dict():
    file_path = os.path.join(settings.BASE_DIR, 'theme', 'templates', 'flashcards', 'hiragana.json')
    with open(file_path, 'r') as file:
        return json.load(file)

def load_katakana_dict():
    file_path = os.path.join(settings.BASE_DIR, 'theme', 'templates', 'flashcards', 'katakana.json')
    with open(file_path, 'r') as file:
        return json.load(file)

# View to create a default deck for a user
def create_default_deck(user):
    if not Deck.objects.filter(name="Japanese Basics").exists():
        japaneseDict = load_japanese_dict()  # Load the Japanese Dictionary
        # Create the default deck
        japanese_basics_deck = Deck.objects.create(name="Japanese Basics", is_default=True)

        # Loop through the dictionary and create flashcards
        for vocab_word, details in japaneseDict.items():
            Card.objects.create(
                deck=japanese_basics_deck,
                vocab_word=vocab_word,
                kana=details['kana'],
                english_translation=details['english_translation'],
                part_of_speech=details['part_of_speech'],
                example_sentence=details['example_sentence'],
                example_sentence_kana=details['example_sentence_kana'],
                example_sentence_english=details['example_sentence_english']
            )


from django.shortcuts import get_object_or_404, redirect, render
from .models import Deck, Card

def edit_deck(request, deck_id):
    # Get the deck without filtering by user, allowing access for logged-out users
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = Card.objects.filter(deck=deck)  # Get all flashcards for the deck

    # Check if the user is authenticated and is the owner of the deck
    is_owner = request.user.is_authenticated and deck.user == request.user

    if request.method == "POST" and is_owner:
        # Handle updates only if the user is the owner
        deck_form = DeckForm(request.POST, instance=deck)
        if deck_form.is_valid():
            deck_form.save()  # Save the updated deck information

        # Handle card deletion if specified
        if 'delete_cards' in request.POST:
            card_ids_to_delete = request.POST.getlist('delete_cards')  # List of card IDs to delete
            Card.objects.filter(id__in=card_ids_to_delete).delete()

        # Process updates for each flashcard
        for flashcard in flashcards:
            flashcard_form = FlashcardForm(request.POST, instance=flashcard)
            if flashcard_form.is_valid():
                flashcard_form.save()

        return redirect('my_decks')  # Redirect to the decks page after saving changes

    else:
        # Prepopulate the form with existing data
        deck_form = DeckForm(instance=deck)
        flashcard_forms = [FlashcardForm(instance=flashcard) for flashcard in flashcards]

    return render(request, 'flashcards/edit_deck.html', {
        'deck_form': deck_form,
        'flashcard_forms': flashcard_forms,
        'deck': deck,
        'flashcards': flashcards,
        'is_owner': is_owner,  # Pass ownership status to the template
    })


def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    deck.delete()  # Delete the deck along with its associated flashcards
    return redirect('my_decks')  # Redirect to the decks page after deletion
