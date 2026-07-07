from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Job, Company
from .forms import JobForm, CompanyForm
from django.http import HttpResponseForbidden


def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query
    })


@login_required
def employer_dashboard(request):
    if request.user.user_type != 'employer':
        return HttpResponseForbidden()
    # Prefetch related applications to avoid N+1 queries
    jobs = Job.objects.filter(employer=request.user).prefetch_related('application_set__applicant')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})


@login_required
def company_profile(request):
    if request.user.user_type != 'employer':
        return HttpResponseForbidden()
    # Show list of companies and allow creating a new one
    companies_qs = Company.objects.filter(employer=request.user).order_by('name')

    # paginate companies
    paginator = Paginator(companies_qs, 10)
    page_number = request.GET.get('page')
    companies = paginator.get_page(page_number)

    edit_id = request.GET.get('edit')
    edit_instance = None
    if edit_id:
        edit_instance = get_object_or_404(Company, id=edit_id, employer=request.user)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=edit_instance)
        if form.is_valid():
            company = form.save(commit=False)
            company.employer = request.user
            company.save()
            return redirect('employer_dashboard')
    else:
        form = CompanyForm(instance=edit_instance)

    return render(request, 'jobs/company_profile.html', {
        'form': form,
        'companies': companies,
        'paginator': paginator,
    })


@login_required
def create_job(request):
    if request.user.user_type != 'employer':
        return HttpResponseForbidden()
    companies = Company.objects.filter(employer=request.user)
    if not companies.exists():
        return redirect('company_profile')

    if request.method == 'POST':
        form = JobForm(request.POST)
        # limit company choices to this user's companies
        form.fields['company'].queryset = companies
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm()
        form.fields['company'].queryset = companies

    return render(request, 'jobs/create_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.employer:
        return HttpResponseForbidden()
    # GET -> show confirmation page; POST -> perform delete
    if request.method == 'GET':
        return render(request, 'jobs/confirm_delete_job.html', {'job': job})

    if request.method == 'POST':
        job.delete()
        return redirect('employer_dashboard')

    return HttpResponseForbidden()


@login_required
def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.user != company.employer:
        return HttpResponseForbidden()
    # GET -> show confirmation page; POST -> delete
    if request.method == 'GET':
        return render(request, 'jobs/confirm_delete_company.html', {'company': company})

    if request.method == 'POST':
        company.delete()
        return redirect('company_profile')

    return HttpResponseForbidden()