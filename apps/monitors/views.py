from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from monitors.models import Monitor
from monitors.serializers import MonitorSerializer
from monitors.permissions import IsOwnerOrReadOnly


class MonitorViewSet(viewsets.ModelViewSet):
    """
    Viewset to list, create, retrieve, update, delete API Monitors
    """

    queryset = Monitor.objects.select_related('user').order_by('-created_at')
    serializer_class = MonitorSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)