import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
    PeriodicTasks
)

from monitors.models import Monitor



@receiver(post_save, sender=Monitor)
def create_task_on_monitor_save(sender, instance, **kwargs):
    """
    If the monitor instance active status has been changed to false, it ignores the instance task.
    If new monitor is created, it creates a PeriodicTask
    """

    task_name = f'monitor-schedule-{instance.id}'

    if not instance.is_active:
        PeriodicTask.objects.filter(name=task_name).update(enabled=False)
        PeriodicTasks.update_changed()
        return

    interval, _ = IntervalSchedule.objects.get_or_create(
        every=instance.interval,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            'interval': interval,
            'task': 'monitoring.tasks.monitor_checker_task',
            'args': json.dumps([instance.id]),
            'enabled': True,
        }
    )

    PeriodicTasks.update_changed()



@receiver(post_delete, sender=Monitor)
def remove_task_on_monitor_delete(sender, instance, **kwargs):
    """
    Removes the PeriodicTask when the monitor instance is deleted.
    """
    PeriodicTask.objects.filter(name=f'monitor-schedule-{instance.id}').delete()
    PeriodicTasks.update_changed()