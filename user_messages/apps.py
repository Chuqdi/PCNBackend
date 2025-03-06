from django.apps import AppConfig


class UserMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_messages"
    
    def ready(self):
        import user_messages.signals
