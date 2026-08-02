from django.db import models
from monitors.models import Monitor


class MonitoringResult(models.Model):
    """
    Result for each api monitor check
    """

    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='monitor_results')

    status_code = models.PositiveIntegerField()
    response_time = models.DurationField()
    is_successful = models.BooleanField()
    error_message = models.TextField(blank=True, null=True)
    checked_at = models.DateTimeField(auto_now_add=True)