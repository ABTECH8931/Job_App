from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

# Create your models here.
#Models for Employer profile
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='company_/logos', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name
    
#Models for JobSeeker profile
class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    skills = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
    
#Function to define where to upload resumes
def resume_upload_path(instance, filename):
    return f'resumes/user_{instance.job_seeker.user.id}/{filename}'

#Function to define where to upload cover letters
def cover_letter_upload(instance, filename):
    return f'cover_letters/user_{instance.job_seeker.user.id}/{filename}'

#Model for job
class Job(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    JOB_TYPE_CHOICES = [
        ('full_time', 'Full_Time'),
        ('part_time', 'Part_Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_posted = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_posted']

#Model for job applications
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to=resume_upload_path) # type: ignore
    cover_letter = models.FileField(upload_to=cover_letter_upload, blank=True, null=True) # type: ignore
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_applied = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.job_seeker.full_name} - {self.job.title}'
    
    class Meta:
        ordering = ['-date_applied']
        unique_together = ('job', 'job_seeker')
    




