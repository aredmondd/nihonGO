from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import Deck, Card
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import json
from .models import Deck
from .forms import DeckForm, FlashcardForm

# Create your views here.
def index (request):
    return render(request, 'index.html')

def register (request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")
        
    
    context = {'registerform':form}
    return render(request, 'register.html', context=context)

def about(request):
    team_members = [
        {'name': 'Alex Richardson', 'image': 'richardson.jpg', 'description': 'actually knows japanese', 'link' : 'https://github.com/lrichardson21'},
        {'name': 'Aiden Redmond', 'image': 'redmond.jpg', 'description': 'made everyone learn tailwind', 'link' : 'https://github.com/aredmondd'},
        {'name': 'Michael Durden', 'image': 'durden.jpg', 'description': 'had to nuke his github branch(es)', 'link' : 'https://github.com/masterjedidcfl'},
        {'name': 'Eunice Ladu', 'image': 'eunice.jpg', 'description': 'tbd', 'link' : 'https://github.com/eunice-rayy'},
    ]
    return render(request, 'about.html', {'team_members': team_members})

def dashboard (request):
    return render(request, 'dashboard.html')

def forum (request):
    return render(request, 'forum.html')

def profile (request):
    return render(request, 'my-profile.html')

def messages (request):
    return render(request, 'messages.html')

# Create your views here.
def home (request):
    return render(request, 'myapp/base.html')

def profile_page (request):
    return render(request, 'myapp/profile-page.html')


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("profile-page")
            
    
    context = {'loginform':form}

    return render(request, 'login.html', {'form': form})


def user_logout(request):

    auth.logout(request)

    return redirect("index")

@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Use BASE_DIR to construct the relative path
file_path = f"{settings.BASE_DIR}/theme/templates/flashcards/japanesebasics.json"

# Open the file using the relative path
with open(file_path, 'r') as file:
    japaneseDict = json.load(file)

def my_decks(request):
    if not request.user.is_authenticated:
        # For non-authenticated users, show a default "Japanese Basics" deck.
        decks = [
            {'id': 1, 'name': 'Japanese Basics', 'cards': load_japanese_dict()},
            {'id': 2, 'name': 'Example Deck 2', 'cards': {}},  # No cards
            {'id': 3, 'name': 'Example Deck 3', 'cards': {}},  # No cards
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
            new_deck.user = request.user
            new_deck.save()

            for flashcard_form in flashcard_forms:
                flashcard = flashcard_form.save(commit=False)
                flashcard.deck = new_deck
                flashcard.save()

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


def study(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)  # This will raise a 404 if the deck doesn't exist
    flashcards = Card.objects.filter(deck=deck)
    
    return render(request, 'flashcards/study.html', {'deck': deck, 'flashcards': flashcards})


def load_japanese_dict():
    with open('/Users/laurenrichardson/Desktop/nihonGO!/nihonGO/nihonGO/theme/templates/flashcards/japanesebasics.json', 'r') as json_file:
        japaneseDict = json.load(json_file)
    return japaneseDict

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