from django.contrib import admin
from .models import Tool, ToolCategory

@admin.register(ToolCategory)
class ToolCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'link')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_select_related = ('category',)
