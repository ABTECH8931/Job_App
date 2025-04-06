from django.contrib import admin
from .models import Employer, JobSeeker, Job, JobApplication

# Register your models here.
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location', 'date_joined')
    search_fields = ('company_name', 'user_username', 'location')

class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'location')
    search_fields = ('full_name', 'user_username', 'skills')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'status', 'date_posted', 'deadline')
    list_filter = ('status', 'job_type', 'location')
    search_fields = ('title', 'description', 'employer_company_name')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display =('job_seeker', 'job', 'status', 'date_applied')
    list_filter = ('status', 'date_applied')
    search_fields = ('job_seeker_full_name', 'job_title')


admin.site.register(Employer, EmployerAdmin)
admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
