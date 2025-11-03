from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Represents a job posting created by an employer.
    """
    employer = models.ForeignKey(
        'accounts.EmployerProfile',
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.employer.company_name}"
    

class Application(models.Model):
    """
    Represents an application made by an employee for a specific job.
    """
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.username} → {self.job.title}"
