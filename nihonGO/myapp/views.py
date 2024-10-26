from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import UpdateUserForm, UpdateProfileForm
from django.urls import reverse_lazy



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

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):

    template_name = 'users/change_password.html'

    success_message = "Successfully Changed Your Password"
    
    success_url = reverse_lazy('users-home')

@login_required
def profile(request):
    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(request, 'Your profile is updated successfully')

            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'templates/profile-page.html', {'user_form': user_form, 'profile_form': profile_form})


