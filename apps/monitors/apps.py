from django.apps import AppConfig


class MonitorsConfig(AppConfig):
    name = 'monitors'

    def ready(self):
        import monitors.signals