import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
try:
    from config.env import env
    settings_module = env('DJANGO_SETTINGS_MODULE')
except (ImportError, NameError):
    settings_module = 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

app = Celery('config')

# Set worker pool
app.conf.update(
    worker_pool='threads',
    worker_concurrency=1,
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()