from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'role_in_the_company', 'is_staff', 'is_admin')
    list_filter = ['is_admin']
    search_fields = ('username','email', 'first_name', 'last_name', 'phone', 'role_in_the_company')
