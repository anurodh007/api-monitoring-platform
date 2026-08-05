from celery import shared_task

from incidents.services import IncidentService


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 5},
    queue='incident_evaluations',
)
def process_monitoring_result_task(payload: dict):
    """
    Celery task that handles failure_streak and Incident creation/updation.
    """
    service = IncidentService()
    service.evaluate_monitoring_result(
        monitor_id=payload['monitor_id'],
        is_successful=payload['is_successful'],
        checked_at=payload['checked_at']
    )