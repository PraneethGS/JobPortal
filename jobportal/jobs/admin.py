from django.contrib import admin
from .models import Job, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name', 'employer')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ('title', 'employer', 'location', 'created_at')
	search_fields = ('title', 'company__name', 'employer__username')
