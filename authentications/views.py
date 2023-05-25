from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    
    form = 'Login'  # Move this line outside the if-else block
    
    return render(request, 'authentications/registration.html', {'form': form})

def LogoutUser(request):
    logout(request)
    return redirect ('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                form.add_error('confirm_password', "Passwords do not match.")
            else:
                # authenticate new user to log in after sign up
                user = authenticate(username=username, password=password)
                # log in the user 
                login(request, user)
                # direct the user to homepage
                return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'authentications/registration.html', {'form': form})
              

def home(request):
    return render(request, 'authentications/home.html' )


