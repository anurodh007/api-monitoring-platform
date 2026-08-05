from django.core.cache import cache
from django.db import transaction

from incidents.models import Incident, IncidentStatus, IncidentSeverity

CACHE_TIMEOUT = 60 * 60 * 24


class IncidentService:

    def get_cache_key(self, monitor_id):
        return f'consecutive_failures_{monitor_id}'

    def get_active_incident(self, monitor_id):
        return Incident.objects.filter(
                    monitor_id=monitor_id,
                    status=IncidentStatus.OPEN,
                    resolved_at__isnull=True
                ).first()

    def get_or_create_active_incident(self, monitor_id):
        with transaction.atomic():
            incident, _ = Incident.objects.get_or_create(
                monitor_id=monitor_id,
                status=IncidentStatus.OPEN,
                resolved_at__isnull=True,
                defaults={
                    'title': f'Incident: Monitor-{monitor_id}'
                }
            )
        return incident

    def get_severity_level(self, failure_streak):
        if failure_streak <= 3:
            return IncidentSeverity.LOW
        elif failure_streak <= 7:
            return IncidentSeverity.MEDIUM
        elif failure_streak <= 10:
            return IncidentSeverity.HIGH
        else:
            return IncidentSeverity.CRITICAL

    def evaluate_monitoring_result(self, monitor_id, is_successful, checked_at):
        cache_key = self.get_cache_key(monitor_id)

        try:
            if is_successful:
                incident = self.get_active_incident(monitor_id)
                cache.delete(key=cache_key)
                if incident:
                    incident.resolve()
                return

            try:
                failure_streak = cache.incr(key=cache_key) or 0
            except ValueError:
                cache.set(cache_key, 1, CACHE_TIMEOUT)
                failure_streak = 1

            if failure_streak < 3:
                return

            incident = self.get_or_create_active_incident(monitor_id)
            incident.failure_count = failure_streak
            incident.severity = self.get_severity_level(failure_streak)
            incident.last_failed_at = checked_at
            incident.save(update_fields=['failure_count', 'severity', 'last_failed_at'])


        except Exception as e:
            raise e