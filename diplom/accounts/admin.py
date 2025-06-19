from django.contrib import admin

from .models import ServicePackage

from .models import Computer, Booking

from .models import Tournament, TournamentRegistration


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

    #tournament

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'start_date', 'end_date', 'status', 'registered_count')
    list_filter = ('game', 'is_active')
    search_fields = ('name', 'game', 'description')
    date_hierarchy = 'start_date'
    filter_horizontal = ()
    ordering = ('-start_date',)

@admin.register(TournamentRegistration)
class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'user', 'registration_date', 'is_confirmed')
    list_filter = ('tournament', 'is_confirmed')
    search_fields = ('user__username', 'tournament__name')