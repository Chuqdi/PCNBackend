from django.apps import AppConfig


class UserNotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_notifications"
    
    def ready(self):
        import user_notifications.signals
