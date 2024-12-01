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
        widget=forms.TextInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm w-full px-12',
            'placeholder': 'Username',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm w-full px-12',
            'placeholder': 'Email',
            'required': True
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm w-full px-12',
            'placeholder': 'Password',
            'required': True
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-black border-2 text-black rounded-lg text-sm w-full px-12',
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
        fields = ['title', 'content'] 
        labels = {
            'title': 'Post Title',  
            'content': "What do you want to know?"
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

# - Update Profiles
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-text form-input block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500'})  
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input-text form-input block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500'})  
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'input-file block w-full text-sm text-gray-500 mt-1'})  
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input-textarea form-textarea block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500', 'rows': 5}) 
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']