from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
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
                'firstname': user.firstname
            }

            if user.user_type == 1:
                return render(request, 'dashboard_admin.html', {'user_info': user_info})
            elif user.user_type == 2:
                return render(request, 'dashboard_customer.html', {'user_info': user_info})
            else:
                return render(request, 'dashboard_employee.html', {'user_info': user_info})

        return render(request, 'login.html', {'login_failed': True})

    return render(request, 'login.html')
