from django.shortcuts import render, redirect
from django.http import HttpResponse

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

def decks (request):
    return render(request, 'mydecks.html')


from .models import Deck
from .forms import DeckForm, FlashcardForm

def add_deck(request):
    if request.method == "POST":
        deck_form = DeckForm(request.POST)
        flashcard_forms = [FlashcardForm(request.POST) for _ in range(int(request.POST.get('num_cards', 0)))]

        if deck_form.is_valid() and all(f.is_valid() for f in flashcard_forms):
            new_deck = deck_form.save(commit=False)
            new_deck.user = request.user  # Associate the deck with the logged-in user
            new_deck.save()  # Save the deck

            # Save flashcards
            for flashcard_form in flashcard_forms:
                flashcard = flashcard_form.save(commit=False)
                flashcard.deck = new_deck  # Associate the flashcard with the new deck
                flashcard.save()

            return redirect('mydecks')  # Redirect to the decks page
    else:
        deck_form = DeckForm()
        flashcard_forms = [FlashcardForm() for _ in range(3)]  # Start with 3 empty flashcard forms

    return render(request, 'flashcards/add_deck.html', {
        'deck_form': deck_form,
        'flashcard_forms': flashcard_forms,
    })

def my_decks(request):
    decks = Deck.objects.filter(user=request.user)  # Get decks for the logged-in user
    return render(request, 'flashcards/mydecks.html', {'decks': decks})