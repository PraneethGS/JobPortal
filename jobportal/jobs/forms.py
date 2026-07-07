from django import forms
from .models import Job, Company


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'title', 'location', 'description']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website']