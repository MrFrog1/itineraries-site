from django.apps import AppConfig

class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'  # Adjust this to match your actual app structure

    def ready(self):
        import customers.signals  # This ensures that the signal is registered