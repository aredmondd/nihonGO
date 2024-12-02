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
        {'name': 'Eunice Ladu', 'image': 'eunice.jpg', 'description': 'cybersecurity & messaging god', 'link' : 'https://github.com/eunice-rayy'},
    ]
    return render(request, 'about.html', {'team_members': team_members})

def dashboard (request):
    return render(request, 'dashboard.html')

from django.db.models import Sum
from django.shortcuts import render
from django.utils.timezone import now
def profile(request):
    user = request.user
    today = now().date()

    # Get all UserCardProgress entries for the user
    user_progress = UserCardProgress.objects.filter(user=user)

    # Reset logic: Check if any `last_reset` is not today
    if not user_progress.filter(last_reset=today).exists():
        # Reset today's progress
        user_progress.update(studied_on=today, last_reset=today)

    # Fetch progress for today
    flashcard_progress_today = UserCardProgress.objects.filter(user=user, studied_on=today)

    # Calculate percentage correct
    total_attempts = flashcard_progress_today.count()
    correct_answers = sum(progress.correctCount for progress in flashcard_progress_today)
    percent_correct = (correct_answers / total_attempts * 100) if total_attempts > 0 else 0

    # Fetch user's forum posts
    forum_posts = user.posts.all()
    total_upvotes = forum_posts.aggregate(total_upvotes=Sum('upvotes'))['total_upvotes'] or 0

    return render(request, 'my-profile.html', {
        'flashcard_progress_today': flashcard_progress_today,
        'percent_correct': percent_correct,
        'forum_posts': forum_posts,
        'total_upvotes': total_upvotes,
    })


def edit_profile (request):
    return render(request, 'myapp/edit_profile.html')

def messages (request):
    return render(request, 'messages.html')

# Create your views here.
def home (request):
    return render(request, 'myapp/base.html')

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

# @login_required
# def profile(request):
#     print("Profile view is running teehee")
#     return render(request, 'my-profile.html')

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
        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.user = request.user
            deck.is_default = False
            deck.save()

            # Process the flashcards
            vocab_words = request.POST.getlist('vocab_word[]')
            kana = request.POST.getlist('kana[]')
            translations = request.POST.getlist('english_translation[]')
            parts_of_speech = request.POST.getlist('part_of_speech[]')
            example_sentences = request.POST.getlist('example_sentence[]')
            example_sentences_kana = request.POST.getlist('example_sentence_kana[]')
            example_sentences_english = request.POST.getlist('example_sentence_english[]')

            for i in range(len(vocab_words)):
                if vocab_words[i]:  # Only add cards with vocab words
                    Card.objects.create(
                        deck=deck,
                        vocab_word=vocab_words[i],
                        kana=kana[i],
                        english_translation=translations[i],
                        part_of_speech=parts_of_speech[i],
                        example_sentence=example_sentences[i],
                        example_sentence_kana=example_sentences_kana[i],
                        example_sentence_english=example_sentences_english[i]
                    )
            return redirect('my_decks')  # Redirect to user's decks page
    else:
        deck_form = DeckForm()

    return render(request, 'flashcards/add_deck.html', {'deck_form': deck_form})

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
from django.utils.timezone import now
from datetime import date

def study(request, deck_id):
    # Get the deck object
    deck = get_object_or_404(Deck, id=deck_id)

    # Initialize context
    context = {
        'deck': deck,
        'flashcards': [],
        'message': None,
        'daily_study_count': 0,
    }

    # For default decks, show all flashcards for logged-out users
    if deck.is_default and not request.user.is_authenticated:
        context['flashcards'] = deck.card_set.all()
        context['message'] = "Log in to enable spaced repetition and save your progress."
        
        return render(request, 'flashcards/study.html', context)

    # For authenticated users
    if request.user.is_authenticated:
        # Check if the user owns the deck (if it's not default)
        if not deck.is_default and deck.user != request.user:
            return redirect('my_decks')

        # Retrieve all cards in the deck
        flashcards = deck.card_set.all()

        # Ensure a `UserCardProgress` entry exists for each card in the deck
        for card in flashcards:
            UserCardProgress.objects.get_or_create(
                user=request.user,
                card=card,
                defaults={
                    'last_reviewed': now(),
                    'next_review_date': now(),
                    'ease_factor': 2.5,
                    'interval': 1,
                    'repetition_count': 0,
                    'correctCount': 0,
                }
            )

        # Filter cards due for review
        current_time = now()
        due_flashcards = flashcards.filter(
            usercardprogress__user=request.user,
            usercardprogress__next_review_date__lte=current_time
        )

        # If no due flashcards, show all cards (optional fallback)
        if not due_flashcards.exists():
            due_flashcards = flashcards

        # Calculate daily study count
        today = date.today()
        daily_study_count = UserCardProgress.objects.filter(
            user=request.user,
            last_reviewed__date=today
        ).count()

        # Update context
        context['flashcards'] = due_flashcards
        context['daily_study_count'] = daily_study_count
        return render(request, 'flashcards/study.html', context)

    # If unauthenticated and the deck is not default
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
        for deck in decks:
            deck.cards = deck.card_set.all()
    else:
        # For authenticated users, show both their decks and the default decks
        decks = Deck.objects.filter(Q(user=request.user) | Q(id__in=[1, 5, 6])).distinct()
        for deck in decks:
            deck.cards = deck.card_set.all()

    return render(request, 'flashcards/mydecks.html', {'decks': decks})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Deck, Card, UserCardProgress
from .forms import DeckForm, FlashcardForm

def edit_deck(request, deck_id):
    # Get the deck without filtering by user, allowing access for logged-out users
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = Card.objects.filter(deck=deck)  # Get all flashcards for the deck

    # Check if the user is authenticated and is the owner of the deck
    is_owner = request.user.is_authenticated and deck.user == request.user
    is_default = deck.is_default
    flashcard_stats = []

    # Fetch progress for each card
    if request.user.is_authenticated:
        progress_data = UserCardProgress.objects.filter(user=request.user, card__in=flashcards)
        progress_dict = {progress.card_id: progress for progress in progress_data}
    else:
        progress_dict = {}

    # Attach progress stats to each flashcard
    for card in flashcards:
        progress = progress_dict.get(card.id)
        flashcard_stats.append({
            'flashcard': card,
            'correct_count': progress.correctCount if progress else 0,
            'incorrect_count': (progress.repetition_count - progress.correctCount) if progress else 0,
        })

    if request.method == "POST" and is_owner:
        # Handle deck updates
        new_deck_name = request.POST.get("deck_name")
        if new_deck_name:
            deck.name = new_deck_name.strip()
            deck.save()
           
        else:
            messages.error(request, "Deck name cannot be empty.")
        

        # Handle card deletion
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
        deck_form = DeckForm(instance=deck)
        flashcard_forms = [FlashcardForm(instance=flashcard) for flashcard in flashcards]

    return render(request, 'flashcards/edit_deck.html', {
        'deck_form': deck_form,
        'flashcard_forms': flashcard_forms,
        'deck': deck,
        'flashcards': flashcards,
        'is_owner': is_owner,
        'is_default': is_default,
        'flashcard_stats': flashcard_stats,  # Include flashcard stats in the context
    })


@login_required
@login_required
def add_cards(request, deck_id):
    # Get the deck and verify ownership
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)

    if request.method == "POST":
        # Extract data from the form submission
        vocab_words = request.POST.getlist('vocab_word[]')
        kana = request.POST.getlist('kana[]')
        english_translations = request.POST.getlist('english_translation[]')
        parts_of_speech = request.POST.getlist('part_of_speech[]')
        example_sentences = request.POST.getlist('example_sentence[]')
        example_sentences_kana = request.POST.getlist('example_sentence_kana[]')
        example_sentences_english = request.POST.getlist('example_sentence_english[]')

        # Ensure that all the fields have the same number of entries
        num_cards = len(vocab_words)
        
        # Loop through the submitted data and create new cards
        for i in range(num_cards):
            Card.objects.create(
                deck=deck,
                vocab_word=vocab_words[i],
                kana=kana[i],
                english_translation=english_translations[i],
                part_of_speech=parts_of_speech[i],
                example_sentence=example_sentences[i],
                example_sentence_kana=example_sentences_kana[i],
                example_sentence_english=example_sentences_english[i]
            )

        return redirect('edit_deck', deck_id=deck.id)  # Redirect to the edit deck page
    else:
        flashcard_form = FlashcardForm()

    return render(request, 'flashcards/add_cards.html', {
        'deck': deck,
        'flashcard_form': flashcard_form,
    })



def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    deck.delete()  # Delete the deck along with its associated flashcards
    return redirect('my_decks')  # Redirect to the decks page after deletion 

def update_progress(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            correct = data.get('correct')

            # Get the UserCardProgress for the given card and user
            progress, created = UserCardProgress.objects.get_or_create(
                user=request.user,
                card_id=card_id,
                defaults={
                    'ease_factor': 2.5,
                    'interval': 1,
                    'repetition_count': 0,
                    'correctCount': 0,
                },
            )

        

            # Update the progress
            progress.update_progress(correct)

            # Increment the daily studied card count (can be tracked in a session or DB)
            request.session['cards_studied_today'] = request.session.get('cards_studied_today', 0) + 1

            return JsonResponse({'status': 'success', 'message': 'Progress updated successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


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

    # Check if the delete button was clicked and the user is the post owner
    if request.method == "POST" and request.user == post.user:
        post.delete()
        return redirect('forum_index') 

    # Handle reply form submission
    elif request.method == 'POST':
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
