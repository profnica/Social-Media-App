from django.shortcuts import render, redirect
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Replace 'success' with the name of your success page
    else:
        form = RegistrationForm()

    return render(request, 'authentications/registeration.html', {'form': form})


def home(request):
    return render(request, 'authentications/home.html')


