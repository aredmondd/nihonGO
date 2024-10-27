from django.shortcuts import render, redirect
from .models import Deck, Flashcard
from .forms import DeckForm, FlashcardForm

def create_deck(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user  # Associate with current user
            deck.save()
            return redirect('deck_list')
    else:
        form = DeckForm()
    return render(request, 'flashcards/createDeck.html', {'form': form})

def deck_list(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'flashcards/deck_list.html', {'decks': decks})

def add_flashcard(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.deck = deck
            flashcard.save()
            return redirect('deck_list')
    else:
        form = FlashcardForm()
    return render(request, 'flashcards/add_flashcard.html', {'form': form, 'deck': deck})
