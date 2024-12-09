from django import forms
from .models import ChatRoom
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'members']  # Adjust fields as necessary

    def clean_name(self):
        name = self.cleaned_data['name']
        # Regex to allow only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', name):
            raise forms.ValidationError(
                "Room name can only contain letters, numbers, and underscores. No spaces or special characters are allowed."
            )
        return name