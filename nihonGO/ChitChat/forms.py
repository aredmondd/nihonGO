from django import forms
from .models import ChatRoom
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'members']  # Adjust fields as necessary

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