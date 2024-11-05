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
from .forms import DeckForm, FlashcardForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

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


def profile (request):
    return render(request, 'my-profile.html')

def edit_profile (request):
    return render(request, 'myapp/edit_profile.html')

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
    return redirect("index")

@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Change password view
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'myapp/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile-page')

# Update profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Initialize forms with POST data and files
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.theme_profile)

        # Check if user form is valid and has changed data
        if user_form.is_valid():
            if user_form.has_changed():  # Only save if there are changes
                user_form.save()

        # Check if profile form is valid and has changed data
        if profile_form.is_valid():
            if profile_form.has_changed():  # Only save if there are changes
                profile_form.save()

        return redirect('profile-page')  # Redirect to profile page after update

    else:
        # GET request - initialize forms with existing user data
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.theme_profile)

    return render(request, 'myapp/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Use BASE_DIR to construct the relative path
file_path = f"{settings.BASE_DIR}/theme/templates/flashcards/japanesebasics.json"

#Open Japanese Basics
with open(file_path, 'r') as file:
    japaneseDict = json.load(file)


def my_decks(request):
    if not request.user.is_authenticated:
        # For non-authenticated users, show a default "Japanese Basics" deck.
       
        decks = [
            {'id': 1, 'name': 'Japanese Basics', 'cards': load_japanese_dict()},
            {'id': 5, 'name': 'Hiragana', 'cards': load_hiragana_dict},  # No cards
            {'id': 6, 'name': 'Katakana', 'cards': load_katakana_dict},  # No cards
        ]
    else:
        # Check if the default deck exists for authenticated users; if not, create it.
        user = request.user
        if not Deck.objects.filter(user=user, is_default=True).exists():
            create_default_deck(user)  # Create the deck for the user.
            create_hiragana_deck(user)
            create_katakana_deck(user)
        
        # Fetch the user's decks including the default deck
        decks = Deck.objects.filter(user=user)
    
    return render(request, 'flashcards/mydecks.html', {'decks': decks})


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

@login_required(login_url='login')
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

DEFAULT_DECKS = ["Japanese Basics", "Hiragana", "Katakana"]
def study(request, deck_id):
    # Get the deck object
    deck = get_object_or_404(Deck, id=deck_id)

    # Check if the deck is a default deck
    if deck.is_default and deck.name in DEFAULT_DECKS:
        # If the user is not logged in, do not apply spaced repetition
        if not request.user.is_authenticated:
            # Return all flashcards in the deck without filtering for spaced repetition
            context = {
                'deck': deck,
                'flashcards': deck.card_set.all()
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

def create_hiragana_deck(user):
    if not Deck.objects.filter(name="Hiragana", user=user).exists():
        hiragana_dict = load_hiragana_dict()  # Load Hiragana Dictionary
        # Create the Hiragana deck
        hiragana_deck = Deck.objects.create(name="Hiragana", user=user, is_default=True)

        # Loop through the dictionary and create flashcards
        for vocab_word, details in hiragana_dict.items():
            Card.objects.create(
                deck=hiragana_deck,
                vocab_word=vocab_word,
                kana=details['kana'],
                english_translation=details['english_translation'],
                part_of_speech=details['part_of_speech'],
                example_sentence=details['example_sentence'],
                example_sentence_kana=details['example_sentence_kana'],
                example_sentence_english=details['example_sentence_english']
            )

def create_katakana_deck(user):
    if not Deck.objects.filter(name="Katakana", user=user).exists():
        katakana_dict = load_katakana_dict()  # Load Katakana Dictionary
        # Create the Katakana deck
        katakana_deck = Deck.objects.create(name="Katakana", user=user, is_default=True)

        # Loop through the dictionary and create flashcards
        for vocab_word, details in katakana_dict.items():
            Card.objects.create(
                deck=katakana_deck,
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


#FORUM VIEWS
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Reply
from .forms import PostForm, ReplyForm  # You'll need to create these forms
from django.contrib.auth.decorators import login_required


# View for the forum index
def forum_index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')  # All posts for logged-in users
    else:
        posts = Post.objects.all().order_by('-created_at')[:50]  # 50 most recent posts for logged-out users
    
    return render(request, 'forum/forumIndex.html', {'posts': posts})

# View for creating a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum_index')
    else:
        form = PostForm()
    return render(request, 'forum/newPost.html', {'form': form})

# View for a specific post and its replies
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all().order_by('-created_at')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.save()
            return redirect('post_detail', post_id=post.id)
    else:
        reply_form = ReplyForm()
    return render(request, 'forum/postDetail.html', {
        'post': post,
        'replies': replies,
        'reply_form': reply_form,
    })

# View for upvoting a post
@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    return redirect('post_detail', post_id=post.id)

def add_reply(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user  # Assuming the user is logged in
            new_reply.post = post
            new_reply.save()
            return redirect('theme:post_detail', post_id=post.id)
    else:
        form = ReplyForm()
    return render(request, 'theme/add_reply.html', {'form': form, 'post': post})

