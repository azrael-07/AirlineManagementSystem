from django.apps import AppConfig


class FlightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.flights'
    def ready(self):
        import apps.flights.signals  # noqa
