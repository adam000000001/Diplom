from django.contrib import admin

from .models import ServicePackage
# Register your models here.

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')