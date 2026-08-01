from django.contrib import admin
from monitors.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'method', 'interval', 'timeout', 'expected_status_code', 'is_active']

    list_editable = ['method', 'interval', 'timeout', 'expected_status_code', 'is_active']

    list_filter = ['method']