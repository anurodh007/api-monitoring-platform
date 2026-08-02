from rest_framework import permissions
from monitors.models import Monitor


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        monitor_id = view.kwargs.get('monitor_id')
        if not monitor_id:
            return False

        monitor = Monitor.objects.get(id=monitor_id)
        return monitor.user == request.user