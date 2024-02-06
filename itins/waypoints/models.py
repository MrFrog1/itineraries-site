from django.db import models
from components.models import Component
from itineraries.models import AgentItinerary, ItineraryDayComponent, ItineraryDay

from django.core.exceptions import ValidationError

# In the frontend, it will look something like this - https://www.alltrails.com/trail/india/ladakh/likir-hemis-shukpachan-via-phobe-la-section


class Waypoint(models.Model):
    # Foreign keys to the related models
    itinerary_day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, null=True, blank=True)
    agent_itinerary = models.ForeignKey(AgentItinerary, on_delete=models.CASCADE, null=True, blank=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, blank=True)
    itinerary_day_component = models.ForeignKey(ItineraryDayComponent, on_delete=models.CASCADE, null=True, blank=True)

    # Additional fields
    google_place_reference = models.CharField(max_length=255)
    place_name = models.CharField(max_length=55)
    description = models.TextField(blank=True, null=True, max_length=120)
    ordering = models.PositiveIntegerField()

    def clean(self):
        # Validation to ensure that a Waypoint is related to only one of the models
        related_objects = [self.itinerary_day, self.agent_itinerary, self.component, self.itinerary_day_component]
        if sum(obj is not None for obj in related_objects) != 1:
            raise ValidationError('A Waypoint must be related to exactly one ItineraryDay, AgentItinerary, Component, or ItineraryDayComponent.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.place_name} (Order: {self.ordering})"