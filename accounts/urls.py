# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration routes
    path('register/employee/', views.register_employee, name='register_employee'),
    path('register/employer/', views.register_employer, name='register_employer'),

    # Authentication routes
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),

    # Employer profile management
    path('employer/profile/', views.manage_employer_profile, name='manage_employer_profile'),
]

