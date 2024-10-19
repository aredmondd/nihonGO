from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import CreateUserForm, LoginForm

# - Authentication Models and Functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

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
