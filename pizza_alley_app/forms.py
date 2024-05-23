from django import forms
from .models import Products, Accounts

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['productID', 'productName', 'price']

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['email', 'firstname', 'lastname', 'user_type', 'profile_picture']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['productID', 'productName', 'price']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
