from django import forms
<<<<<<< HEAD
from .models import Accounts, Orders
=======
from .models import Accounts
>>>>>>> 8a1263d (Arziel Coddess)
from .models import Products
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
        fields = ['firstname', 'lastname', 'email', 'user_type']

<<<<<<< HEAD

=======
>>>>>>> 8a1263d (Arziel Coddess)
# Lawas, Arziel Mae L. - part

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
<<<<<<< HEAD
        fields = ['productID', 'productName', 'price']


# Delgado, Donnell Keith D. - part

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['employeeID', 'employeeName', 'totalSales']

=======
        fields = ['productID', 'productName', 'price']
>>>>>>> 8a1263d (Arziel Coddess)
