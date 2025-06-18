from django.contrib import admin

from .models import ServicePackage

from .models import Computer, Booking
# Register your models here.

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name', 'description')

#Бронирование

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'computer', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'computer')
    search_fields = ('user__username', 'computer__name')
    date_hierarchy = 'start_time'