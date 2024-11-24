from django.apps import AppConfig


class PcnConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "PCNs"
    
    def ready(self) -> None:
        import PCNs.signals
