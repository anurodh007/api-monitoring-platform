import django_filters
from datetime import datetime, time
from monitoring.models import MonitoringResult


class MonitoringResultFilter(django_filters.FilterSet):
    passed = django_filters.BooleanFilter(field_name='is_successful', label='Passed')
    date = django_filters.DateFilter(method='filter_by_date_onwards', label='Date')

    class Meta:
        model = MonitoringResult
        fields = {}

    def filter_by_date_onwards(self, queryset, name, value):
        if not value:
            return queryset
        start_of_day = datetime.combine(value, time.min)
        return queryset.filter(checked_at__gte=start_of_day)