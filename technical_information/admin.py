from django.contrib import admin
from .models import (
    TestingAccountEnvironment, TestingAccount,
    SyntheticEventTarget, SyntheticEventType, SyntheticEvent
)


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


@admin.register(SyntheticEventTarget)
class SyntheticEventTargetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SyntheticEventType)
class SyntheticEventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(SyntheticEvent)
class SyntheticEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'target')
    list_filter = ('event_type', 'target')
    search_fields = ('name', 'description')
    list_select_related = ('event_type', 'target')
