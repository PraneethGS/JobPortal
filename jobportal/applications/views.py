from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Application
from .forms import ApplicationForm
from jobs.models import Job
import os
from django.conf import settings


@login_required
def apply_job(request, job_id):
    if request.user.user_type != 'jobseeker':
        return HttpResponseForbidden("Only jobseekers can apply.")

    job = get_object_or_404(Job, id=job_id)

    existing = Application.objects.filter(job=job, applicant=request.user).first()
    if existing:
        # If an application already exists, redirect the user to edit it so they can update/replace resume
        return redirect('edit_application', app_id=existing.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'applications/my_applications.html', {'applications': applications})


@login_required
def application_detail(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Only the applicant or the job's employer can view the application
    if request.user != application.applicant and request.user != application.job.employer:
        return HttpResponseForbidden("Not allowed.")

    return render(request, 'applications/application_detail.html', {'app': application})


@login_required
def delete_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    # Only the applicant may delete their application
    if request.user != application.applicant:
        return HttpResponseForbidden("Not allowed.")

    if request.method == 'POST':
        # delete associated file if present
        if application.resume:
            try:
                application.resume.delete(save=False)
            except Exception:
                pass
        application.delete()
        return redirect('my_applications')

    return render(request, 'applications/confirm_delete.html', {'app': application})

@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.employer:
        return HttpResponseForbidden("Not allowed.")

    applications = Application.objects.filter(job=job)

    return render(request, 'applications/view_applicants.html', {
        'job': job,
        'applications': applications
    })


@login_required
def update_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.job.employer:
        return HttpResponseForbidden("Not allowed.")

    new_status = request.POST.get('status')
    application.status = new_status
    application.save()

    return redirect('view_applicants', job_id=application.job.id)


@login_required
def edit_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.user != application.applicant:
        return HttpResponseForbidden("Not allowed.")

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            # If a new resume file was uploaded, delete the old file first
            if 'resume' in request.FILES and application.resume:
                try:
                    application.resume.delete(save=False)
                except Exception:
                    pass
            form.save()
            return redirect('application_detail', app_id=application.id)
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'applications/apply_job.html', {'form': form, 'job': application.job, 'editing': True})