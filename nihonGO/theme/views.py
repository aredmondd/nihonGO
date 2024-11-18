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
from django.contrib.auth import authenticate, login
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
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("my-profile")

    context = {'registerform': form}
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


def profile(request):
    user = request.user
    profile = profile.objects.get(user=user)
    
    # Fetch user-specific flashcard progress and statistics
    flashcard_progress = UserCardProgress.objects.filter(user=user)
    
    # Fetch user's forum posts
    forum_posts = Post.objects.filter(user=user)
    
    return render(request, 'my-profile.html', {
        'profile': profile,
        'flashcard_progress': flashcard_progress,
        'forum_posts': forum_posts,
    })

def edit_profile (request):
    return render(request, 'myapp/edit_profile.html')

def messages (request):
    return render(request, 'messages.html')

# Create your views here.
def home (request):
    return render(request, 'myapp/base.html')


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

                return redirect("my-profile")
            
    
    context = {'loginform':form}

    return render(request, 'login.html', {'form': form})


def user_logout(request):

    auth.logout(request)

    return redirect("index")

@login_required
def profile(request):
    return render(request, 'my-profile.html')

# Change password view
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'myapp/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('my-profile')

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

        return redirect('my-profile')  # Redirect to profile page after update

    else:
        # GET request - initialize forms with existing user data
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.theme_profile)

    return render(request, 'myapp/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#Use BASE_DIR to construct the relative path
file_path = f"{settings.BASE_DIR}/theme/templates/flashcards/japanesebasics.json"

#Open Japanese Basics
with open(file_path, 'r') as file:
    japaneseDict = json.load(file)

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

from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Deck, UserCardProgress

def study(request, deck_id):
    # Get the deck object
    deck = get_object_or_404(Deck, id=deck_id)

    # Initialize context with the deck and empty flashcards list
    context = {
        'deck': deck,
        'flashcards': [],
        'message': None,
    }

    # For default decks, show all flashcards for logged-out users
    if deck.is_default:
        if not request.user.is_authenticated:
            # Show all flashcards in the deck for logged-out users
            context['flashcards'] = deck.card_set.all()
            context['message'] = "Log in to enable spaced repetition and save your progress."
            return render(request, 'flashcards/study.html', context)

    # For authenticated users or non-default decks
    if request.user.is_authenticated:
        # Check if the user owns the deck if it's not default
        if not deck.is_default and deck.user != request.user:
            return redirect('my_decks')  # Redirect unauthorized access to the user's deck list

        # Retrieve all flashcards in the deck
        flashcards = deck.card_set.all()

        # Apply spaced repetition for authenticated users on non-default decks
        if not deck.is_default:
            current_time = timezone.now()
            flashcards = flashcards.filter(
                usercardprogress__user=request.user,
                usercardprogress__next_review_date__lte=current_time
            )

        # Update the context with filtered flashcards
        context['flashcards'] = flashcards
        return render(request, 'flashcards/study.html', context)

    # If an unauthenticated user tries to access a non-default deck
    context['message'] = "Please log in to access this deck."
    return render(request, 'flashcards/study.html', context)




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
def create_default_deck():
    if not Deck.objects.filter(name="Japanese Basics").exists():
        japaneseDict = load_japanese_dict()  # Load the Japanese Dictionary
        # Create the default deck
        #japanese_basics_deck = Deck.objects.create(name="Japanese Basics", is_default=True)
        japanese_basics_deck = Deck.objects.create(
                id=1,  # Assign a fixed ID
                name="Japanese Basics", 
                is_default=True,
            )

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

        return japanese_basics_deck

def create_hiragana_deck():
    if not Deck.objects.filter(name="Hiragana").exists():
        hiragana_dict = load_hiragana_dict()  # Load Hiragana Dictionary
        # Create the Hiragana deck
        #hiragana_deck = Deck.objects.create(name="Hiragana", is_default=True)
        hiragana_deck = Deck.objects.create(
                id=4,  # Assign a fixed ID
                name="Hiragana", 
                is_default=True
            )
        

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
        return hiragana_deck

def create_katakana_deck():
    if not Deck.objects.filter(name="Katakana").exists():
        katakana_dict = load_katakana_dict()  # Load Katakana Dictionary
        # Create the Katakana deck
        #katakana_deck = Deck.objects.create(name="Katakana", is_default=True)
        katakana_deck = Deck.objects.create(
                id=6,  # Assign a fixed ID
                name="Katakana", 
                is_default=True
            )

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
        return katakana_deck

from django.shortcuts import get_object_or_404, redirect, render
from .models import Deck, Card
from django.db.models import Q
DEFAULT_DECKS = ["Japanese Basics", "Hiragana", "Katakana"]
def my_decks(request):
    create_default_deck()
    create_hiragana_deck()
    create_katakana_deck()

    if not request.user.is_authenticated:
        # For non-authenticated users, only show the default decks
        decks = Deck.objects.filter(id__in=[1, 5, 6])  # Fetch only default decks with fixed IDs (1, 5, 6)
    else:
        # For authenticated users, show both their decks and the default decks
        decks = Deck.objects.filter(Q(user=request.user) | Q(id__in=[1, 5, 6])).distinct()
        for deck in decks:
            deck.cards = deck.card_set.all()

    return render(request, 'flashcards/mydecks.html', {'decks': decks})

def edit_deck(request, deck_id):
    # Get the deck without filtering by user, allowing access for logged-out users
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = Card.objects.filter(deck=deck)  # Get all flashcards for the deck

    # Check if the user is authenticated and is the owner of the deck
    is_owner = request.user.is_authenticated and deck.user == request.user
    is_default = deck.is_default

    if request.method == "POST" and is_owner and is_default:
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
        'is_default': is_default,
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
            # Redirect to the post_detail view for the newly created post
            return redirect('post_detail', post_id=post.id)
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
from django.views.decorators.http import require_POST
@login_required
@require_POST  # Ensure this view is accessed only via POST requests
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    return JsonResponse({'upvotes': post.upvotes}) 

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

