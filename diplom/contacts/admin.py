from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'phone', 'email', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('club_name', 'address', 'phone', 'email', 'opening_hours')
        }),
        ('Социальные сети', {
            'fields': ('social_facebook', 'social_vk', 'social_telegram', 'social_instagram'),
            'classes': ('collapse',)
        }),
        ('Карта', {
            'fields': ('map_embed_code',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )