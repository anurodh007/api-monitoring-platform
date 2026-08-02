from django.contrib import admin
from monitoring.models import MonitoringResult


@admin.register(MonitoringResult)
class MonitoringResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'monitor', 'status_code', 'response_time', 'is_successful', 'error_message', 'checked_at']

    list_filter = ['is_successful']