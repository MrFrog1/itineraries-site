from django.db import models
from hotels.models import Hotel
from itineraries.models import AgentItinerary
from django.conf import settings

# Create your models here.
class Likes(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='user_feed_likes_customer')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    original_agent_itinerary = models.ForeignKey(AgentItinerary, null=True, blank= True, on_delete=models.CASCADE)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name ='user_feed_likes_agent')

class Dislike(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='user_feed_dislikes_customer')
    hotel = models.ForeignKey(Hotel, null=True, blank= True, on_delete=models.CASCADE)
    original_agent_itinerary = models.ForeignKey(AgentItinerary,  null=True, blank= True, on_delete=models.CASCADE)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank= True, on_delete=models.CASCADE, related_name ='user_feed_dislikes_agent')


class Saved_for_Later(models.Model):
    itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)