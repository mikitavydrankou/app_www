from django.contrib import admin

from .models import PentestRecord


@admin.register(PentestRecord)
class PentestRecordAdmin(admin.ModelAdmin):
    list_display = ('target', 'operation', 'user', 'status', 'success', 'created_at')
    list_filter = ('operation', 'status', 'success', 'created_at')
    search_fields = ('target', 'user__username', 'task_id')
    readonly_fields = ('created_at', 'completed_at', 'task_id')
    
    fieldsets = (
        ('Target Info', {
            'fields': ('user', 'target', 'operation'),
        }),
        ('Task Status', {
            'fields': ('task_id', 'status', 'success'),
        }),
        ('Results', {
            'fields': ('latency_ms', 'result_data', 'error_message'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
        }),
    )
