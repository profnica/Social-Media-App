from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from authentications.authentication import EmailAuthBackend
from .forms import RegistrationForm
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.urls import reverse
from .models import Profile, CustomUser


# User= get_user_model()

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Create an instance of the EmailAuthBackend
        email_auth_backend = EmailAuthBackend()
        
        # authenticate user if the user exist in the db
        user = email_auth_backend.authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend' )
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
            
    # Create an instance of the LoginForm
    form = 'Login'  # Move this line outside the if-else block
    
    return render(request, 'authentications/registration.html', {'form': form})

def LogoutUser(request):
    logout(request)
    return redirect ('home')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            
            # to save user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # to save user profile 
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            return render(request, 'authentications/register_done.html', {'form': form, 'profile_form': profile_form})
    else:
        form = RegistrationForm()
        profile_form = ProfileEditForm()
    
    return render(request, 'authentications/registration.html', {'form': form, 'profile_form': profile_form})

def forgetpassword(request):
    print("Inside forgetpassword view")  # Add this print statement
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            subject = 'Reset Your Password'
            message = render_to_string('authentications/reset_password_email.html',{
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
        password1 = request.POST['password1']
        remember_me = request.POST.get('remember_me', False)

        user = auth.authenticate(username=username, password1=password1)

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

# to allow user alone to edit their profile, we will use decorator
# Edit view
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile = Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('home')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileEditForm(instance=request.user.profile)
        else:
            profile = Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=profile)

    return render(request, 'authentications/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
