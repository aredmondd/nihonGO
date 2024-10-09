from django.shortcuts import render
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
    return render(request, 'decks.html')