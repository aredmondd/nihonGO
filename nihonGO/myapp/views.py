from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home (request):
    return render(request, 'myapp/base.html')

def profile_page (request):
    return render(request, 'myapp/profile-page.html')


def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("my-login")
        
    
    context = {'registerform':form}
    return render(request, 'myapp/register.html', context=context)


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

    return render(request, 'myapp/login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("home")

@login_required
def profile(request):
    return render(request, 'users/profile.html')






DEEPL_API_KEY = 'your-deepl-api-key'
DEEPL_API_URL = 'https://api-free.deepl.com/v2/translate'  # Adjust for pro users

def deepl_translate_view(request):
    translated_text = None
    if request.method == 'POST':
        input_text = request.POST.get('text')
        target_lang = request.POST.get('target_lang', 'EN')  # Default to English if no language is selected

        # Ensure only English and Japanese are allowed
        if target_lang not in ['EN', 'JA']:
            target_lang = 'EN'  # Fallback to English if an invalid option is passed

        # Prepare the DeepL API request
        data = {
            'auth_key': DEEPL_API_KEY,
            'text': input_text,
            'target_lang': target_lang
        }

        # Make the request to DeepL API
        response = requests.post(DEEPL_API_URL, data=data)

        # Parse the response from DeepL
        if response.status_code == 200:
            translated_text = response.json().get('translations')[0].get('text')

    return render(request, 'translate.html', {'translated_text': translated_text})