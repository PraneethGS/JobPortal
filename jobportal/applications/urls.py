from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my/', views.my_applications, name='my_applications'),
    path('view/<int:job_id>/', views.view_applicants, name='view_applicants'),
    path('update/<int:app_id>/', views.update_status, name='update_status'),
    path('detail/<int:app_id>/', views.application_detail, name='application_detail'),
    path('delete/<int:app_id>/', views.delete_application, name='delete_application'),
    path('edit/<int:app_id>/', views.edit_application, name='edit_application'),
]