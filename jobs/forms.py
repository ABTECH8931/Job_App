from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Employer, JobSeeker, Job, JobApplication

#User registration form for both employer and job seeker 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#Employer registration form
class EmployerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'website', 'location', 'phone', 'logo']

#JobSeeker registration form
class JobSeekerRegistrationForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['full_name', 'bio', 'location', 'phone', 'skills']

#Job creation form
class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'salary', 'location', 'job_type', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

#Job application form
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

#Search form for jobs 
class JobSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search jobs...'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Location...'}))
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + list(Job.JOB_TYPE_CHOICES))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

