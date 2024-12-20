from django.apps import AppConfig


class DiscountCodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'discount_codes'
    
    def ready(self):
        import discount_codes.signals
