from django.apps import AppConfig


class VotantesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'votantes'

    def ready(self):
        import votantes.signals
