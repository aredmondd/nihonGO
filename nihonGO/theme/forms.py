# forms.py
from django import forms
from .models import Deck, Card, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['vocab_word', 'kana', 'english_translation', 'part_of_speech', 'example_sentence', 'example_sentence_kana', 'example_sentence_english']

# - Create/Register a user (Model Form)
class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Username',
            'required': True
        })
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Email',
            'required': True
        })
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Password',
            'required': True
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Confirm Password',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# - Authenticate a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'username',
            'id': 'username',
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Username',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'username',
            'id': 'username',
            'class': 'border border-black border-2 text-black rounded-lg text-sm',
            'placeholder': 'Password',
            'required': True
        })
    )


#FORUM
from django import forms
from .models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

from django import forms
from .models import Post, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Adjust fields as needed

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']