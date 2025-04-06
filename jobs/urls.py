from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #common urls
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('register/employer/', views.employer_register, name='employer_register'),
    path('register/jobseeker/', views.jobseeker_register, name='jobseeker_register'),
    

    #authentication urls
    path('login/employer/', auth_views.LoginView.as_view(template_name='employer/login.html'), name='employer_login'),
    path('login/jobseeker/', auth_views.LoginView.as_view(template_name='jobseeker/login.html'), name='jobseeker_login'),
    path('logout/', views.user_logout, name='logout'),

    #employer urls
    path('employer/register/', views.employer_register, name='employer_register'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/jobs/create/', views.create_job, name='create_job'),
    path('employer/jobs/<int:job_id>/update/', views.update_job, name='update_job'),
    path('employer/jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('employer/jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('employer/applications/<int:application_id>/update_status/', views.update_application_status, name='update_application_status'),
    path('employer/profile/update/', views.update_employer_profile, name='update_employer_profile'),
    path('employer/delete/', views.delete_employer_profile, name='delete_employer_profile'),

    #job seeker urls
    path('jobseeker/register/', views.jobseeker_register, name='jobseeker_register'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('jobseeker/applications/', views.jobseeker_applications, name='jobseeker_applications'),
    path('jobseeker/profile/update/', views.update_jobseeker_profile, name='update_jobseeker_profile'),
    path('jobseeker/delete/', views.delete_jobseeker_profile, name='delete_jobseeker_profile'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('profile/<int:job_seeker_id>/', views.view_job_seeker_profile, name='view_job_seeker_profile'),

    #password reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]