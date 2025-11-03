from django.contrib import admin

from .models import PingRecord


@admin.register(PingRecord)
class PingRecordAdmin(admin.ModelAdmin):
	list_display = ('domain', 'user', 'success', 'latency_ms', 'created_at')
	list_filter = ('success', 'created_at')
	search_fields = ('domain', 'user__username')
