from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib import messages, auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse


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
                 # Create the new user
                user = User.objects.create_user(username=username, password=password)
                # authenticate new user to log in after sign up
                user = authenticate(username=username, password=password)
                # log in the user 
                login(request, user)
                # direct the user to homepage
                return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'authentications/registration.html', {'form': form})


def forgetpassword(request):
    
    print("Inside forgetpassword view")  # Add this print statement
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            subject = 'Reset Your Password'
            message = render_to_string('authentications/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            email = EmailMessage(subject, message, to=[email])
            email.send()
            messages.success(request, 'Password reset link sent to your email.')
            
            print("Redirection to reset-instruction should occur here")
            return redirect('reset-instruction') 
        else:
            messages.error(request, 'User with this email address does not exist.')

    return render(request, 'authentications/password-reset.html')

def reset_instruction(request):
    return render(request, 'authentications/reset_instructions.html')
    

def RememberMe(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)

            if not remember_me:
                request.session.set_expiry(0)  # Session expires when the browser is closed
            else:
                request.session.set_expiry(604800)  # Session expires in 7 days (adjust as needed)

            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/registration.html')

def home(request):
    return render(request, 'authentications/home.html' )

def dashboard(request):
    return render(request,'authentications/dashboard.html')
