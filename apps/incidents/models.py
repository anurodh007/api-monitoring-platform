from django.db import models
from django.utils import timezone
from monitors.models import Monitor


class IncidentSeverity(models.TextChoices):
    """
    Severity levels for an incident
    """
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'


class IncidentStatus(models.TextChoices):
    """
    Status of an incident
    """
    OPEN = 'OPEN'
    RESOLVED = 'RESOLVED'


class Incident(models.Model):
    """
    Incident model for a service problem
    """
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='incidents')

    title = models.CharField(max_length=100)

    status = models.CharField(
        max_length=10,
        choices=IncidentStatus.choices,
        default=IncidentStatus.OPEN
    )

    severity = models.CharField(
        max_length=10,
        choices=IncidentSeverity.choices,
        default=IncidentSeverity.LOW,
        db_index=True
    )

    failure_count = models.PositiveIntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    last_failed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['monitor', 'status']),
        ]

    def __str__(self):
        return f'[{self.severity}] {self.title} ({self.status})'

    def resolve(self):
        """
        Mark incident as resolved with accurate timestamp.
        """
        if self.status != IncidentStatus.RESOLVED:
            self.status = IncidentStatus.RESOLVED
            self.resolved_at = timezone.now()
            self.save(update_fields=['status', 'resolved_at'])