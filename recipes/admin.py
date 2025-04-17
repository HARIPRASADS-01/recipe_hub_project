# recipes/admin.py
from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'description', 'ingredients', 'instructions', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('title', 'author', 'description', 'image')}),
        ('Content', {'fields': ('ingredients', 'instructions')}),
        ('Timings (minutes)', {'fields': ('prep_time', 'cook_time')}),
        ('Metadata', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )