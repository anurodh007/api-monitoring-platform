from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monitors.views import MonitorViewSet

from monitoring.views import (
    MonitoringCheckAPIView,
    MonitoringResultsListAPIView
)


router = DefaultRouter()
router.register(r'', MonitorViewSet, basename='monitor'),


urlpatterns = [
    # api/monitors/ and api/monitors/{id}/
    *router.urls,

    # api/monitors/<int:monitor_id>/check/
    path('<int:monitor_id>/check/', MonitoringCheckAPIView.as_view(), name='monitor-check'),

    # api/monitors/<int:monitor_id>/results/
    path('<int:monitor_id>/results/', MonitoringResultsListAPIView.as_view(), name='monitor-results'),
]