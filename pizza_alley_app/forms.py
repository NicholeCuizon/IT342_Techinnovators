from django import forms
from .models import Accounts
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AccountUpdateForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        (0, 'Employee'),
        (1, 'Admin')
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='User Type')

    class Meta:
        model = Accounts
        fields = ['firstname', 'lastname', 'email', 'user_type', 'profile_picture']

