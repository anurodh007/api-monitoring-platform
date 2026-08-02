from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from monitors.models import Monitor
from monitors.serializers import MonitorSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """
    Viewset to list, create, retrieve, update, delete API Monitors
    """

    queryset = Monitor.objects.select_related('user')
    serializer_class = MonitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)