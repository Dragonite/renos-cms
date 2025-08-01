from django.contrib import admin
from .models import TestingAccountEnvironment, TestingAccount


@admin.register(TestingAccountEnvironment)
class TestingAccountEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TestingAccount)
class TestingAccountAdmin(admin.ModelAdmin):
    list_display = ('label', 'username', 'environment', 'is_active')
    list_filter = ('environment', 'is_active')
    search_fields = ('label', 'username', 'description')
    list_select_related = ('environment',)
    list_editable = ('is_active',)
