from django.shortcuts import get_object_or_404

from rest_framework import generics

from monitors.models import Monitor

from monitoring.models import MonitoringResult
from monitoring.serializers import MonitoringResultSerializer
from monitoring.services import check_api_status
from monitoring.permissions import IsOwner
from monitoring.filters import MonitoringResultFilter



class MonitoringCheckAPIView(generics.CreateAPIView):
    """
    Allows the authenticated owner to check individual API Monitor status
    """

    queryset = MonitoringResult.objects.select_related('monitor__user')
    serializer_class = MonitoringResultSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        """
        Calls check_api_status service and save the serialized data
        """
        monitor_id = self.kwargs.get('monitor_id')
        monitor = get_object_or_404(Monitor, id=monitor_id)

        data = check_api_status(monitor_id)
        serializer.save(monitor=monitor, **data)



class MonitoringResultsListAPIView(generics.ListAPIView):
    """
    Allows the authenticated owner to view the results history of an API Monitor
    """

    queryset = MonitoringResult.objects.select_related('monitor__user')
    serializer_class = MonitoringResultSerializer
    permission_classes = [IsOwner]
    filterset_class = MonitoringResultFilter

    def get_queryset(self):
        monitor_id = self.kwargs.get('monitor_id')
        return self.queryset.filter(monitor__id=monitor_id).order_by('-checked_at')