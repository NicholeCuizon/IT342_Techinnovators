from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login, name='login'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_employee/', views.dashboard_employee, name='dashboard_employee'),
    path('dashboard_customer/', views.dashboard_customer, name='dashboard_customer'),
]
