# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, EmployerProfile, EmployeeProfile


class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's default UserCreationForm to include an email field
    and connect it to our custom User model.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class EmployerProfileForm(forms.ModelForm):
    """
    Form for creating or updating Employer profile information.
    """
    class Meta:
        model = EmployerProfile
        fields = ['company_logo', 'company_name', 'company_description', 'company_location']


class EmployeeProfileForm(forms.ModelForm):
    """
    Form for creating or updating Employee profile information.
    """
    class Meta:
        model = EmployeeProfile
        fields = [
            'full_name', 'mobile', 'location',
            'summary', 'resume', 'skills', 'education', 'projects'
        ]
