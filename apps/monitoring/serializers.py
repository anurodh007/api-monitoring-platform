from rest_framework import serializers
from monitoring.models import MonitoringResult


class MonitoringResultSerializer(serializers.ModelSerializer):
    monitor = serializers.CharField(source='monitor.name', read_only=True)

    class Meta:
        model = MonitoringResult
        fields = [
            'id',
            'monitor',
            'status_code',
            'response_time',
            'is_successful',
            'error_message',
            'checked_at',
        ]
        read_only_fields = [
            'id',
            'status_code',
            'response_time',
            'is_successful',
            'error_message',
            'checked_at',
        ]