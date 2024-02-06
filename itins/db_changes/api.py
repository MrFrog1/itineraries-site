from rest_framework import viewsets
from .models import DbChange
from itineraries.models import ItineraryDayComponent

from .serializers import DbChangeSerializer


class DbChangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DbChangeSerializer

    def get_queryset(self):
        user = self.request.user

        # Query all changes made by the user
        user_changes = DbChange.objects.filter(user=user)

        # Additional query for ItineraryDayComponent changes where the user is either the agent or the customer
        if hasattr(user, 'agent') or hasattr(user, 'customer'):
            component_changes = ItineraryDayComponent.objects.filter(
                itinerary_day__itinerary_group__itinerarygrouping__customer_itinerary__agent=user.agent
            ) | ItineraryDayComponent.objects.filter(
                itinerary_day__itinerary_group__itinerarygrouping__customer_itinerary__customer=user.customer
            )

            # Combine the user's changes with ItineraryDayComponent changes where they're involved
            user_changes = user_changes | DbChange.objects.filter(description__in=component_changes, changed_model='ItineraryDayComponent')

        return user_changes