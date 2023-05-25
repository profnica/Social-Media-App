from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password
