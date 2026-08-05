from django.urls import reverse, reverse_lazy

from rest_framework import serializers
from incidents.models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    monitor_url = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = [
            'id',
            'monitor',
            'monitor_url',
            'title',
            'status',
            'severity',
            'failure_count',
            'started_at',
            'resolved_at',
            'last_failed_at',
        ]

    def get_monitor_url(self, obj):
        request = self.context.get('request')
        relative_url = reverse('monitor-detail', kwargs={'pk': obj.monitor_id})
        if request is not None:
            return request.build_absolute_uri(relative_url)
        return relative_url