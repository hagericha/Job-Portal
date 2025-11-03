# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser and adds a 'role' field
    to differentiate between Employer and Employee.
    """
    EMPLOYER = 'employer'
    EMPLOYEE = 'employee'

    ROLE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (EMPLOYEE, 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class EmployerProfile(models.Model):
    """
    Profile model for Employers — stores company details.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField(blank=True)
    company_location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.company_name


class EmployeeProfile(models.Model):
    """
    Profile model for Employees — stores personal and professional details.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills or short list")
    education = models.TextField(blank=True, help_text="Add education entries (one per line)")
    projects = models.TextField(blank=True, help_text="Add project entries (one per line)")

    def __str__(self):
        return self.full_name or self.user.username

