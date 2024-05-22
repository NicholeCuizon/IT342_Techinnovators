from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login, name='login'),
    path('customer_registration/', views.registration_customer, name='registration_customer'),
    path('employee_registration/', views.registration_employee, name='registration_employee'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_employee/', views.dashboard_employee, name='dashboard_employee'),
    path('dashboard_customer/', views.dashboard_customer, name='dashboard_customer'),
    path('dashboard_admin/pizza_employeeOrder', views.pizza_employeeOrder, name='pizza_employeeOrder'),
    path('add_product/', views.add_product, name='add_product'),  # Correct view for add_product
    path('pizza_employeeOrder/', views.pizza_employeeOrder, name='pizza_employeeOrder'),  # Correct view for add_product
]