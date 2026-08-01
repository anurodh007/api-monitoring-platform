from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ApiMethod(models.TextChoices):
    """
    Choices for REST API Methods
    """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class Monitor(models.Model):
    """
    APIs that are to be monitored
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitors')

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    method = models.CharField(
        max_length=10,
        choices=ApiMethod.choices,
        default=ApiMethod.GET
    )

    interval = models.PositiveIntegerField(help_text='Interval in minutes', default=5)
    timeout = models.PositiveIntegerField(help_text='Timeout in seconds', default=10)

    expected_status_code = models.PositiveIntegerField(default=200)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.method} - {self.name}'