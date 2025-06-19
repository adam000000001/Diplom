from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'is_published')
    list_filter = ('is_published', 'rating')
    search_fields = ('user__username', 'comment')
    list_editable = ('is_published',)
    actions = ['publish_selected', 'unpublish_selected']
    
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Снять с публикации выбранные отзывы"