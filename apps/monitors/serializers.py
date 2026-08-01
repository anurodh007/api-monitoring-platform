from rest_framework import serializers
from monitors.models import Monitor


class MonitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monitor
        fields = [
            'id',
            'name',
            'url',
            'method',
            'interval',
            'timeout',
            'expected_status_code',
            'is_active'
        ]
        read_only_fields = ['id']