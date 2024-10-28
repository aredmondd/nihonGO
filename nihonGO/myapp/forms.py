from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput
from .models import Profile

# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']



# - Authenticate a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

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

