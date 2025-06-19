from django.contrib import admin
from .models import Platform, ServicePackage, Order

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_duration_display', 'is_active', 'is_popular')
    list_filter = ('is_active', 'is_popular')
    filter_horizontal = ('platforms',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'platform', 'status', 'created_at')
    list_filter = ('status', 'platform')
    search_fields = ('user__username', 'package__name')