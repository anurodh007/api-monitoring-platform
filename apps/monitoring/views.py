from django.db import transaction
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

    serializer_class = MonitoringResultSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        """
        Calls check_api_status service and save the serialized data
        """
        data = check_api_status(self.monitor)

        with transaction.atomic():
            serializer.save(monitor=self.monitor, **data)



class MonitoringResultsListAPIView(generics.ListAPIView):
    """
    Allows the authenticated owner to view the results history of an API Monitor
    """

    queryset = MonitoringResult.objects.select_related('monitor__user')
    serializer_class = MonitoringResultSerializer
    permission_classes = [IsOwner]
    filterset_class = MonitoringResultFilter

    def get_queryset(self):
        return self.queryset.filter(monitor_id=self.monitor.id).order_by('-checked_at')