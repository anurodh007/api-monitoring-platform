import json

from celery import shared_task

from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
    PeriodicTasks
)

from monitors.models import Monitor

from monitoring.models import MonitoringResult
from monitoring.services import check_api_status

ACTIVE_MONITORS_KEY = 'active_monitors'
TIME_TO_LIVE = 60 * 60 * 24



@shared_task
def monitor_checker_task(monitor_id):
    """
    Celery task that checks one monitor and creates monitoring result
    """
    if not Monitor.objects.filter(id=monitor_id, is_active=True).exists():
        return None

    data = check_api_status(monitor_id)
    return MonitoringResult.objects.create(
        monitor_id=monitor_id,
        **data
    )



@shared_task
def monitor_dispatcher_task():
    """
    Celery task that finds active monitors and dispatches each monitor for api check
    """

    monitors = Monitor.objects.filter(is_active=True).values('id', 'interval')

    for monitor in monitors:
        interval, _ = IntervalSchedule.objects.get_or_create(
            every=monitor['interval'],
            period=IntervalSchedule.MINUTES,
        )

        PeriodicTask.objects.update_or_create(
            name=f'monitor-schedule-{monitor["id"]}',
            defaults={
                'interval': interval,
                'task': 'monitoring.tasks.monitor_checker_task',
                'args': json.dumps([monitor['id']]),
                'enabled': True,
            }
        )

    PeriodicTasks.update_changed()
    return len(monitors)