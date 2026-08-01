from django.urls import path, include
from rest_framework.routers import DefaultRouter
from monitors.views import MonitorViewSet


urlpatterns = [

]


router = DefaultRouter()
router.register('', MonitorViewSet, basename='monitor'),

urlpatterns += router.urls