from django.contrib import admin

from .models import (
    Country, Application, City, NewsLetter, Contact
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'tagline', 'is_active', 'created_on')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'language', 'currency', 'phone_code', 'is_available', 'is_active', 'created_on')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active', 'created_on']


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_on']
    search_fields = ['email']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'is_active', 'created_on']
    search_fields = ['name', 'email', 'phone_number']
    list_filter = ['created_on']
    list_per_page = 10
    ordering = ['created_on']
    readonly_fields = ['created_on']
    fieldsets = (
        ('Contact Details', {
            'fields': ('name', 'email', 'phone_number', 'message')
        }),
        ('Additional Details', {
            'fields': ('is_active', 'created_on')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone_number', 'message', 'is_active', 'created_on')
        }),
    )
