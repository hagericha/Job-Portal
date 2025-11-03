# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from .forms import CustomUserCreationForm, EmployerProfileForm
from .models import User, EmployeeProfile


# -----------------------------
# Registration Views
# -----------------------------
def register_employee(request):
    """Handle registration for employee users."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.EMPLOYEE
            user.save()
            messages.success(request, "Employee account created. Please log in.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Employee'})


def register_employer(request):
    """Handle registration for employer users."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.EMPLOYER
            user.save()
            messages.success(request, "Employer account created. Please log in.")
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': 'Employer'})


# -----------------------------
# Dashboard Routing
# -----------------------------
def dashboard(request):
    """Redirect user to appropriate dashboard based on role."""
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == User.EMPLOYER:
        return redirect('accounts:employer_dashboard')
    return redirect('accounts:employee_dashboard')


# -----------------------------
# Employer Dashboard
# -----------------------------
def employer_dashboard(request):
    """Employer dashboard for managing company info."""
    if not request.user.is_authenticated or request.user.role != User.EMPLOYER:
        return redirect('accounts:login')

    profile = getattr(request.user, 'employerprofile', None)

    if request.method == 'POST':
        # Update profile fields
        profile.company_name = request.POST.get('company_name', '')
        profile.company_description = request.POST.get('company_description', '')
        profile.company_location = request.POST.get('company_location', '')

        # Handle logo upload/removal
        if 'company_logo' in request.FILES:
            profile.company_logo = request.FILES['company_logo']
        elif 'remove_logo' in request.POST:
            profile.company_logo = None

        profile.save()
        return redirect('accounts:employer_dashboard')

    return render(request, 'accounts/employer_dashboard.html', {'profile': profile})


# -----------------------------
# Employee Dashboard
# -----------------------------
def employee_dashboard(request):
    """Employee dashboard for managing personal information."""
    if not request.user.is_authenticated or request.user.role != User.EMPLOYEE:
        return redirect('accounts:login')

    profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Basic details
        profile.full_name = request.POST.get('full_name', '').strip()
        profile.mobile = request.POST.get('mobile', '').strip()
        profile.location = request.POST.get('location', '').strip()
        profile.summary = request.POST.get('summary', '').strip()

        # Resume handling
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        elif 'remove_resume' in request.POST:
            profile.resume = None

        # Skills / Education / Projects
        profile.skills = request.POST.get('skills', '').strip()
        profile.education = request.POST.get('education', '').strip()
        profile.projects = request.POST.get('projects', '').strip()

        profile.save()
        return redirect('accounts:employee_dashboard')

    # Prepare lists for display
    skills_list = [s.strip() for s in (profile.skills or '').split(',') if s.strip()]
    education_list = [line.strip() for line in (profile.education or '').splitlines() if line.strip()]
    projects_list = [line.strip() for line in (profile.projects or '').splitlines() if line.strip()]

    return render(request, 'accounts/employee_dashboard.html', {
        'profile': profile,
        'skills_list': skills_list,
        'education_list': education_list,
        'projects_list': projects_list,
    })


# -----------------------------
# Logout View
# -----------------------------
def logout_view(request):
    """Handle AJAX logout requests."""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


# -----------------------------
# Employer Profile Management
# -----------------------------
def manage_employer_profile(request):
    """Allow employer to edit their company profile."""
    if not request.user.is_authenticated or request.user.role != User.EMPLOYER:
        return redirect('accounts:login')

    profile = getattr(request.user, 'employerprofile', None)
    form = EmployerProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        employer_profile = form.save(commit=False)
        employer_profile.user = request.user
        employer_profile.save()
        return redirect('accounts:employer_dashboard')

    return render(request, 'accounts/manage_employer_profile.html', {'form': form})
