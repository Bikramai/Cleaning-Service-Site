from django.contrib import admin

from .models import (
    Service, ServiceCategory, ServiceRequest
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_active', 'created_on']
    fieldsets = [
        ('', {'fields': ['name', 'category','price', 'description']}),
        ('content', {'fields': ['content', 'image', 'background_image']}),
    ]


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available', 'is_active', 'created_on']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'phone', 'city', 'country', 'status', 'created_on', 'is_paid'
    ]
    list_filter = ['status', 'is_paid']
    search_fields = ['name', 'email', 'city__name', 'country__name']
    list_per_page = 10
    ordering = ['-created_on']
    date_hierarchy = 'created_on'