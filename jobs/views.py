from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Employer, JobSeeker, Job, JobApplication
from .forms import (UserRegisterForm, EmployerRegistrationForm, JobSeekerRegistrationForm, JobCreationForm, JobApplicationForm, JobSearchForm)

# Create your views here.
# Homepage view
def home(request):
    recent_jobs = Job.objects.filter(status='active').order_by('-date_posted')[:5]
    job_count = Job.objects.filter(status='active').count()  # Count of active jobs
    jobseeker_count = JobSeeker.objects.count()  # Total number of job seekers
    employer_count = Employer.objects.count() # Total number of employers (companies)
    context = {
        'recent_jobs': recent_jobs,
        'job_count': job_count,
        'jobseeker_count': jobseeker_count,
        'employer_count': employer_count,
    }
    return render(request, 'home.html', context)
#about 
def about(request):
    context = {
        'title': 'About Us',
        'description': 'We are a leading job board connecting employers and job seekers.'
    }
    return render(request, 'about.html', context)

#contact
def contact(request):
    context = {
        'title': 'Contact Us',
    }
    return render(request, 'contact.html', context)

#Job listing view
def job_list(request):
    job_list = Job.objects.all()
    form = JobSearchForm(request.GET)  # Bind the form with GET data

    if form.is_valid():
        search_term = form.cleaned_data.get('search')
        if search_term:
            job_list = job_list.filter(title__icontains=search_term)  # Filter by title
            # You can add more filters here based on other fields like description, etc.

        location = form.cleaned_data.get('location')
        if location:
            job_list = job_list.filter(location__icontains=location)

        job_type = form.cleaned_data.get('job_type')
        if job_type:
            job_list = job_list.filter(job_type=job_type)

        salary_range = form.cleaned_data.get('salary_range')
        if salary_range:
            min_salary, max_salary = map(int, salary_range.split('-')) if '-' in salary_range else (int(salary_range[:-1]), float('inf'))
            if max_salary == float('inf'):
                job_list = job_list.filter(salary__gte=min_salary)
            else:
                job_list = job_list.filter(salary__gte=min_salary, salary__lte=max_salary)

    paginator = Paginator(job_list, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        # 'categories': Category.objects.all(), # If you have categories
    }
    return render(request, 'jobs/job_list.html', context)

#Job detail view
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, status='active')
    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'jobseeker'):
        has_applied = JobApplication.objects.filter(
            job=job,
            job_seeker=request.user.jobseeker
        ).exists()
    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)

# Employer registration view
def employer_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = EmployerRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, 'Employer account created successfully!')
            return redirect('employer_dashboard')
    else: 
        user_form = UserRegisterForm()
        profile_form = EmployerRegistrationForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Employer Registration',
    }
    # Change this line to point to your new template
    return render(request, 'employer/register.html', context)

# Job seeker registration view
def jobseeker_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = JobSeekerRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, 'Job seeker account created successfully!')
            return redirect('jobseeker_dashboard')
    else:
        user_form = UserRegisterForm()
        profile_form = JobSeekerRegistrationForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Job Seeker Registration',
        'is_employer': False  # Add this flag for template differentiation
    }
    return render(request, 'jobseeker/register.html', context)


#Employer dashboard
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')

    employer = request.user.employer
    jobs = Job.objects.filter(employer=employer).order_by('-date_posted')
    active_jobs_count = jobs.filter(status='active').count()

    # Correct way to get total applications for the employer's jobs
    total_applications = JobApplication.objects.filter(job__employer=employer).count()

    # Correct way to get recent applications for the employer's jobs
    recent_applications = JobApplication.objects.filter(job__employer=employer).order_by('-date_applied')[:5]

    context = {
        'employer': employer,
        'jobs': jobs[:5],
        'active_jobs_count': active_jobs_count,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
    }
    return render(request, 'employer/dashboard.html', context)

#Job seeker dashboard
@login_required
def jobseeker_dashboard(request):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'You do not have a job seeker profile!')
        return redirect('home')
    
    jobseeker = request.user.jobseeker
    applications = JobApplication.objects.filter(job_seeker=jobseeker).order_by('-date_applied')
    recent_jobs = Job.objects.filter(status='active').order_by('-date_posted')[:5]
    context = {
        'jobseeker': jobseeker,
        'applications': applications[:5],
        'total_applications': applications.count(),
        'recent_jobs': recent_jobs,
    }
    return render(request, 'jobseeker/dashboard.html', context)

#create job view
@login_required
def create_job(request):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    
    if request.method == "POST":
        form = JobCreationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else: 
        form = JobCreationForm()
    context = {
        'form': form,
        'title': 'Post a New Job',
    }
    return render(request, 'employer/create_job.html', context)

#update job view
@login_required
def update_job(request, job_id):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer)

    if request.method == 'POST':
        form = JobCreationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Updated Successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobCreationForm(instance=job)
    context = {
        'form': form,
        'title': 'Update Job',
        'job': job,
    }
    return render(request, 'employer/update_job.html', context)

#delete job view
@login_required
def delete_job(request, job_id):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer) 

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('employer_dashboard')
    context = {
        'job': job,
        'title': 'Delete Job',
    }
    return render(request, 'employer/delete_job.html', context)

#view job applications
@login_required
def view_applications(request, job_id):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer) 
    applications = JobApplication.objects.filter(job=job).order_by('-date_applied')
    context = {
        'job': job,
        'applications': applications,
        'title': f'Applications for {job.title}',
    }
    return render(request, 'employer/view_applications.html', context)

#update application status 
@login_required
def update_application_status(request, application_id):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    
    application = get_object_or_404(JobApplication, id=application_id, job_employer=request.user.employer)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(JobApplication.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, 'Application status updated succesfully!')
        else: 
            messages.error(request, 'Invalid status!')
    return redirect('view_applications', job_id=application.job.id)

#apply for job view
@login_required
def apply_job(request, job_id):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'You do not have a job seeker profile!')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id, status='active')
    jobseeker = request.user.jobseeker

    if JobApplication.objects.filter(job=job, job_seeker=jobseeker).exists():
        messages.warning(request, 'You have already applied for this job!')
        return redirect('job_detail', job_id=job.id)
    
    if request.method =='POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = jobseeker
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobseeker_dashboard')
    else: 
        form = JobApplicationForm()
    context = {
        'form': form,
        'job': job,
        'title': f'Apply for {job.title}',
    }
    return render(request, 'jobs/job_apply.html', context)

#view job seeker application
@login_required
def jobseeker_applications(request):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'You do not have a job seeker profile')
        return redirect('home')
    
    applications = JobApplication.objects.filter(job_seeker=request.user.jobseeker).order_by('-date_applied')
    context = {
        'applications': applications,
        'title': 'My Job Applications',
    }
    return render(request, 'jobseeker/applications.html', context)

#update employer profile
@login_required
def update_employer_profile(request):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    
    employer = request.user.employer 

    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employer_dashboard')
    else:
            form = EmployerRegistrationForm(instance=employer)
    context = {
            'form': form,
            'title': 'Update Profile',
        }
    return render(request, 'employer/update_profile.html', context)

#update job seeker profile
@login_required
def update_jobseeker_profile(request):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'You do not have a job seeker profile')
        return redirect('home')
    
    jobseeker = request.user.jobseeker

    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST, instance=jobseeker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('jobseeker_dashboard')
    else:
        form = JobSeekerRegistrationForm(instance=jobseeker)
    context = {
        'form': form,
        'title': 'Update Profile',
    }
    return render(request, 'jobseeker/update_profile.html', context)

#delete employer profile 
@login_required
def delete_employer_profile(request):
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'You do not have an employer profile!')
        return redirect('home')
    user = request.user

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted!')
        return redirect('home')
    context = {
        'title': 'Delete Account',
    }
    return render(request, 'employer/delete_profile.html', context)

#delete job seeker profile
@login_required
def delete_jobseeker_profile(request):
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'You do not have a job seeker profile!')
        return redirect('home')
    user = request.user

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted!')
        return redirect('home')
    context = {
        'title': 'Delete Account',
    }
    return render(request, 'jobseeker/delete_profile.html', context)

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def delete_jobseeker_profile(request):
    try:
        jobseeker = get_object_or_404(JobSeeker, user=request.user)
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your profile has been successfully deleted.")
        return redirect('home')  # Redirect to your homepage or a confirmation page
    except JobSeeker.DoesNotExist:
        messages.error(request, "Job Seeker profile not found.")
        return redirect('profile') # Redirect to the profile page or an error page
    except Exception as e:
        messages.error(request, f"An error occurred while deleting your profile: {e}")
        return redirect('profile') # Redirect to the profile page or an error page

@login_required
def delete_employer_profile(request):
    try:
        employer = get_object_or_404(Employer, user=request.user)
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your profile has been successfully deleted.")
        return redirect('home')  # Redirect to your homepage or a confirmation page
    except Employer.DoesNotExist:
        messages.error(request, "Employer profile not found.")
        return redirect('profile') # Redirect to the profile page or an error page
    except Exception as e:
        messages.error(request, f"An error occurred while deleting your profile: {e}")
        return redirect('profile') # Redirect to the profile page or an error page

@login_required
def view_job_seeker_profile(request, job_seeker_id):
    job_seeker = get_object_or_404(JobSeeker, id=job_seeker_id)
    job_id = request.GET.get('job_id')
    context = {'job_seeker': job_seeker, 'job_id': job_id}
    return render(request, 'profile/job_seeker_profile.html', context)

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user == job.employer.user:
        if request.method == 'POST':
            job.delete()
            messages.success(request, 'Your job has been successfully deleted.')  # Add success message
            return redirect('employer_dashboard')
        else:
            return redirect('employer_dashboard') # Or handle other methods appropriately
    else:
        return render(request, 'error_page.html', {'message': 'You are not authorized to delete this job.'})