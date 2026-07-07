from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('company/', views.company_profile, name='company_profile'),
    path('create/', views.create_job, name='create_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('company/delete/<int:company_id>/', views.delete_company, name='delete_company'),
]