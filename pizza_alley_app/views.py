from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm, AccountUpdateForm
from django.db.models import Q

#import models
from .models import Accounts, CurrentOrder, Products

#import forms
from .forms import LoginForm

# Cuizon, Nichole P. - Part
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if the user exists in the database
        user = Accounts.objects.filter(email=email, password=password).first()
        if user:
            # Password is correct, log in the user
            request.session['user_email'] = email

            # Get the user's information
            user_info = {
                'firstname': user.firstname,
                'profile_picture': user.profile_picture.url if user.profile_picture else 'default-profile.png'
            }

            if user.user_type == 1:
                return render(request, 'dashboard_admin.html', {'user_info': user_info})
            elif user.user_type == 2:
                return render(request, 'dashboard_customer.html', {'user_info': user_info})
            else:
                return render(request, 'dashboard_employee.html', {'user_info': user_info})

        return render(request, 'login.html', {'login_failed': True})

    return render(request, 'login.html')

def registration_customer(request):
    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        # Convert first name and last name to title case
        firstname = firstname.title()
        lastname = lastname.title()

        # validate email
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return render(request, 'registration_customer.html', {'error': 'Invalid email address'})

        # Proceed with saving data to the database
        obj = Accounts()
        obj.email = email
        obj.firstname = firstname
        obj.lastname = lastname
        obj.password = password
        obj.save()
       
        # Redirect to the login page after successful registration
        return redirect('login')  # Replace 'login' with the actual URL name for your login page

    context = {}

    return render(request, 'registration_customer.html', context)

def registration_employee(request):

    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user_type = request.POST['user_type']
        password = request.POST['password']
 
        # Save data to db
        obj = Accounts()
        obj.email = email
        obj.firstname = firstname
        obj.lastname = lastname
        obj.user_type = user_type
        obj.password = password
        obj.save()
       
        # Redirect to the login page 
        return redirect('login') 
 
    context = {}
 
    return render(request, 'registration_employee.html', context)

def logout(request):
    print("Entering logout view")
    if 'user_email' in request.session:
        del request.session['user_email']
        print("User logged out successfully")
    else:
        print("User is not logged in")
    return redirect('login')

def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

def dashboard_employee(request):
    return render(request, 'dashboard_employee.html')

def dashboard_customer(request):
    return render(request, 'dashboard_customer.html')

def update_account(request, email):
    account = get_object_or_404(Accounts, email=email)

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account for {account.firstname} has been updated.')
            return redirect('account_list') 
    else:
        form = AccountUpdateForm(instance=account)

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'admin/update_account.html', context)

def delete_account(request, email):
    account = get_object_or_404(Accounts, email=email)
    if request.method == 'POST':
        account.delete()
        messages.success(request, f'Account for {account.firstname} has been deleted.')
        return redirect('account_list')  # Replace with the name of the view that lists accounts
    return render(request, 'admin/delete_account.html', {'account': account})

def account_list(request):
    query = request.GET.get('search','')
    if query:
        accounts = Accounts.objects.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query)
        )
    else:
        accounts = Accounts.objects.all()
    return render(request, 'admin/account_list.html', {'accounts': accounts})

# Delgado 

@csrf_exempt
def pizza_employeeOrder(request):
    if request.method == 'POST':
        if 'remove_item' in request.POST:
            currentid = request.POST.get('id')
            currentorder = CurrentOrder.objects.get(id=currentid)
            currentorder.delete()

            return redirect('pizza_employeeOrder')

        elif 'add_item' in request.POST:
            product_id = request.POST.get('product_id')
            quantitypost = request.POST.get('quantity')

            product = Products.objects.get(productID=product_id)

            order = CurrentOrder(productID=product_id,item=product.productName, quantity=quantitypost, price = product.price, total=product.price * int(quantitypost))
            order.save()

            return redirect('pizza_employeeOrder')
    
    else:  #Get request
        products = Products.objects.all()
        current_order = CurrentOrder.objects.all()  
        total = sum(order.total for order in current_order)

        return render(request, 'pizza_employeeOrder.html', {'products': products, 'current_order': current_order, 'total': total})
    
       
# Lawas, Arziel Mae L. - part

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Product added successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error: Form is not valid'})
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
