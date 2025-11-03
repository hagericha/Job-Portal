from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """
    Form for employers to create or edit job postings.
    """
    class Meta:
        model = Job
        fields = ['title', 'location', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
        }
