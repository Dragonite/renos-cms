from django.contrib import admin
from .models import Tool, ToolCategory, ImportantLinks, LinkCategory, Role, TeamMember

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

@admin.register(LinkCategory)
class LinkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ImportantLinks)
class ImportantLinksAdmin(admin.ModelAdmin):
    list_display = ('label', 'category', 'link')
    list_filter = ('category',)
    search_fields = ('label',)
    list_select_related = ('category',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'image', 'role')
    list_filter = ('role',)
    search_fields = ('name', 'email')
    list_select_related = ('role',)
