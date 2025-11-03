from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Job, Application
from .forms import JobForm
from accounts.models import EmployerProfile
from django.contrib.auth import get_user_model

User = get_user_model()


def create_job(request):
    """
    Allows an employer to post a new job.
    - Only accessible to authenticated employers.
    - Requires completed EmployerProfile.
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role != 'employer':
        return redirect('accounts:dashboard')

    employer_profile = getattr(request.user, 'employerprofile', None)
    if employer_profile is None:
        messages.error(request, "Please complete your company profile first.")
        return redirect('accounts:employer_dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer_profile
            job.save()
            messages.success(request, "Job posted successfully.")
            return redirect('accounts:employer_dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})


def delete_job(request, job_id):
    """
    Allows an employer to delete a job they created.
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role != 'employer':
        return redirect('accounts:dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Allow only job owner to delete
    if job.employer.user != request.user:
        messages.error(request, "You don’t have permission to delete this job.")
        return redirect('accounts:employer_dashboard')

    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('accounts:employer_dashboard')

    return redirect('accounts:employer_dashboard')


def job_list(request):
    """
    Displays all job listings to employees and visitors.
    """
    jobs = Job.objects.select_related('employer').order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def apply_job(request, job_id):
    
    job = get_object_or_404(Job, id=job_id)

    # User must be logged in
    if not request.user.is_authenticated:
        messages.error(request, "Please sign in to apply.")
        return redirect('accounts:login')

    # Only employees can apply
    if request.user.role != User.EMPLOYEE:
        messages.error(request, "Only job seekers can apply.")
        return redirect('accounts:dashboard')

    # Prevent duplicate applications
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect('jobs:job_list')

    # Handle POST request (apply button clicked)
    if request.method == 'POST':
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, "Application submitted successfully.")
        return redirect('jobs:job_list')

    # Redirect all non-POST requests back to job list
    return redirect('jobs:job_list')



def my_applications(request):
    """
    Shows the list of jobs the current employee has applied for.
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role != User.EMPLOYEE:
        return redirect('accounts:dashboard')

    applications = (
        Application.objects
        .filter(applicant=request.user)
        .select_related('job__employer')
        .order_by('-created_at')
    )
    return render(request, 'jobs/my_applications.html', {'applications': applications})


def job_applicants(request, job_id):
    """
    Allows an employer to view all applicants for their job posting.
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role != 'employer':
        return redirect('accounts:dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Only allow employer who owns the job
    if job.employer.user != request.user:
        messages.error(request, "You don't have permission to view these applicants.")
        return redirect('accounts:employer_dashboard')

    applicants = job.applications.select_related('applicant').order_by('-created_at')
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applicants': applicants})
