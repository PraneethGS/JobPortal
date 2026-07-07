from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
	fieldsets = UserAdmin.fieldsets + (('Extra', {'fields': ('user_type',)}),)