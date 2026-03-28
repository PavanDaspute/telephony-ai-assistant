"""
Django admin registration for the Property model.
"""

from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "location", "bedrooms", "price", "carpet_area", "created_at"]
    list_filter = ["location", "bedrooms"]
    search_fields = ["title", "location", "description"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
