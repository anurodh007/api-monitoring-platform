from django.contrib import admin
from incidents.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'severity', 'failure_count', 'last_failed_at']