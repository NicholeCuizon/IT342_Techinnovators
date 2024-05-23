from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import ProductUpdateForm, AccountUpdateForm, ProductForm, LoginForm
from .models import Accounts, CurrentOrder, Products
from .decorators import accounts_login_required
from functools import wraps

# Cuizon, Nichole P. - Part
def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

def login_view(request):  # Renamed to avoid conflict with django.contrib.auth.login
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

            # Redirect to the 'next' parameter if it exists
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)

            # Redirect to the respective dashboard based on user type
            if user.user_type == 1:
                return redirect('dashboard_admin')
            elif user.user_type == 2:
                return redirect('dashboard_customer')
            else:
                return redirect('dashboard_employee')

        return render(request, 'login.html', {'login_failed': True})

    # Get the 'next' parameter from the GET request
    next_url = request.GET.get('next')
    return render(request, 'login.html', {'next': next_url})

def registration_customer(request):
    if request.method == 'POST':
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        # Convert first name and last name to title case
        firstname = firstname.title()
        lastname = lastname.title()

        # Validate email
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
        return redirect('login')

    return render(request, 'registration_customer.html')

@accounts_login_required
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
 
    return render(request, 'registration_employee.html')

def logout_view(request):
    try:
        del request.session['user_email']
    except KeyError:
        pass
    return redirect('login')

@accounts_login_required
def dashboard_admin(request):
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    else:
        return render(request, 'dashboard_admin.html')

@accounts_login_required
def dashboard_employee(request):
    return render(request, 'dashboard_employee.html')

@accounts_login_required
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

def update_product(request, productID):
    product = get_object_or_404(Products, productID=productID)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product for {product.productName} has been updated.')
            return redirect('product_list')
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'admin/update_product.html', context)

def delete_account(request, email):
    account = get_object_or_404(Accounts, email=email)
    if request.method == 'POST':
        account.delete()
        messages.success(request, f'Account for {account.firstname} has been deleted.')
        return redirect('account_list')
    return render(request, 'admin/delete_account.html', {'account': account})

def delete_product(request, productID):
    product = get_object_or_404(Products, productID=productID)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product for {product.productName} has been deleted.')
        return redirect('product_list')
    return render(request, 'admin/delete_product.html', {'product': product})

@accounts_login_required
def account_list(request):
    query = request.GET.get('search', '')
    if query:
        accounts = Accounts.objects.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query)
        )
    else:
        accounts = Accounts.objects.all()
    return render(request, 'admin/account_list.html', {'accounts': accounts})

@accounts_login_required
def product_list(request):
    query = request.GET.get('search', '')
    if query:
        products = Products.objects.filter(
            productName__icontains=query
        )
    else:
        products = Products.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

# Delgado 

@csrf_exempt
@accounts_login_required
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

            product = get_object_or_404(Products, productID=product_id)

            order = CurrentOrder(productID=product_id, item=product.productName, quantity=quantitypost, price=product.price, total=product.price * int(quantitypost))
            order.save()

            return redirect('pizza_employeeOrder')
    
    else:  # GET request
        products = Products.objects.all()
        current_order = CurrentOrder.objects.all()
        total = sum(order.total for order in current_order)

        return render(request, 'pizza_employeeOrder.html', {'products': products, 'current_order': current_order, 'total': total})
    
# Lawas, Arziel Mae L. - part
@accounts_login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Product added successfully'})
        else:
            print(form.errors)  # Add this line to print form errors in the console
            return JsonResponse({'status': 'error', 'message': 'Error: Form is not valid', 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

