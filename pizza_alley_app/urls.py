from django.urls import path
from . import views

urlpatterns = [
    # Cuizon, Nichole P. - Part
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),  # Renamed view function
    path('customer_registration/', views.registration_customer, name='registration_customer'),
    path('employee_registration/', views.registration_employee, name='registration_employee'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_employee/', views.dashboard_employee, name='dashboard_employee'),
    path('dashboard_customer/', views.dashboard_customer, name='dashboard_customer'),
    path('accounts/', views.account_list, name='account_list'),
    path('products/', views.product_list, name='product_list'),
    path('accounts/update/<str:email>/', views.update_account, name='update_account'),
    path('accounts/delete/<str:email>/', views.delete_account, name='delete_account'),
    path('products/update/<str:productID>/', views.update_product, name='update_product'),
    path('products/delete/<str:productID>/', views.delete_product, name='delete_product'),
    path('logout/', views.logout_view, name='logout'),

    # Assigned Member??
    path('dashboard_admin/pizza_employeeOrder', views.pizza_employeeOrder, name='pizza_employeeOrder'),

    # Lawas, Arziel Mae L.
    path('add_product/', views.add_product, name='add_product'),  # Correct view for add_product
    path('pizza_employeeOrder/', views.pizza_employeeOrder, name='pizza_employeeOrder'), 
]
