from django.db import models
from customers.models import Customer, Agent
from hotels.models import Hotel
from itineraries.models import AgentItinerary

# Create your models here.
class Likes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    original_agent_itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)
    ageht = models.ForeignKey(Agent, on_delete=models.CASCADE)

class Dislike(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    original_agent_itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)
    ageht = models.ForeignKey(Agent, on_delete=models.CASCADE)


class Saved_for_Later(models.Model):
    itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE)