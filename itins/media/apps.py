from django.apps import AppConfig

print("Importing MediaConfig")

class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media'
    
    def ready(self):
        print("MediaConfig is ready")