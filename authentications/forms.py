import re
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    name= forms.CharField(max_length=100)
    email=forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        if password:
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
                raise forms.ValidationError("Password must contain at least 8 characters, including at least one letter, one number, and one symbol.")

    def save(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        User.objects.create_user(name=name, email=email, username=username, password=password)
