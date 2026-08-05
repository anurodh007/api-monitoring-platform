from rest_framework import viewsets

from incidents.models import Incident
from incidents.serializers import IncidentSerializer


class IncidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Incident.objects.select_related('monitor__user')
    serializer_class = IncidentSerializer
    filterset_fields = ['status', 'severity']

    def get_queryset(self):
        return self.queryset.filter(monitor__user_id=self.request.user.id).order_by('-started_at')