# forms.py
from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password']
