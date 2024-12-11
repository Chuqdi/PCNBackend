from django.apps import AppConfig


class SubscriptionEmailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription_email'
    
    def ready(self):
        import subscription_email.signals
