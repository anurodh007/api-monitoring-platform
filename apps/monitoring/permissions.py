from rest_framework import permissions
from monitors.models import Monitor


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        monitor_id = view.kwargs.get('monitor_id')
        if not monitor_id:
            return False

        try:
            view.monitor = Monitor.objects.select_related('user').get(id=monitor_id)
        except Monitor.DoesNotExist:
            return False

        return view.monitor.user == request.user