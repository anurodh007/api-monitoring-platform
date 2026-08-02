import requests
from django.shortcuts import get_object_or_404
from monitors.models import Monitor, ApiMethod

REQUEST_MAPPING = {
    ApiMethod.GET: lambda u, timeout: requests.get(u, timeout=timeout),
    ApiMethod.DELETE: lambda u, timeout: requests.delete(u, timeout=timeout),
    ApiMethod.POST: lambda u, timeout: requests.post(u, json={}, timeout=timeout),
    ApiMethod.PUT: lambda u, timeout: requests.put(u, json={}, timeout=timeout),
    ApiMethod.PATCH: lambda u, timeout: requests.patch(u, json={}, timeout=timeout),
}


def check_api_status(monitor_or_id):
    """
    Checks the api status of the requested Monitor instance or ID
    """

    if isinstance(monitor_or_id, Monitor):
        monitor= monitor_or_id
    else:
        monitor = get_object_or_404(Monitor.objects.select_related('user'), id=monitor_or_id)

    url = monitor.url
    method = monitor.method
    timeout = monitor.timeout
    expected_status_code = monitor.expected_status_code

    if method in REQUEST_MAPPING:
        try:
            response = REQUEST_MAPPING[method](url, timeout)

            is_successful = (response.status_code == expected_status_code)
            error_message = None if is_successful else response.reason

            return {
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'is_successful': is_successful,
                'error_message': error_message,
            }

        except requests.RequestException as e:
            return {
                'status_code': 0,
                'response_time': 0.0,
                'is_successful': False,
                'error_message': str(e),
            }