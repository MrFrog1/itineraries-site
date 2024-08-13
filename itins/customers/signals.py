from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserAgent

@receiver(post_save, sender=User)
def create_or_update_user_agent(sender, instance, created, **kwargs):
    if instance.is_agent:
        UserAgent.objects.get_or_create(user=instance)