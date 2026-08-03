from django.shortcuts import get_object_or_404

from celery import shared_task

from monitors.models import Monitor

from monitoring.models import MonitoringResult
from monitoring.services import check_api_status



@shared_task
def monitor_checker_task(monitor_id):
    monitor = get_object_or_404(Monitor.objects.select_related('user'), id=monitor_id)

    data = check_api_status(monitor_id)
    return MonitoringResult.objects.create(
        monitor=monitor,
        **data
    )