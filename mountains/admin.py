from django.contrib import admin
from .models import Mountain
@admin.register(Mountain)
class MountainAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "altitude", "difficulty", "featured")
    prepopulated_fields = {"slug": ("name",)}
