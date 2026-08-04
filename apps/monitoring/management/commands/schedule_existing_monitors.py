from django.core.management import BaseCommand

from monitors.models import Monitor

from monitoring.tasks import monitor_dispatcher_task


class Command(BaseCommand):

    help = 'Trigger the initial monitor_dispatcher that schedules tasks for existing monitors'

    def handle(self, *args, **options):
        result = monitor_dispatcher_task()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully synchronized schedules for {result} active monitors.')
        )