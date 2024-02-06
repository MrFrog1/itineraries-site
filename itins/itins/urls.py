"""
URL configuration for itins project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from customers.api import MyTokenObtainPairView, RegisterView, getProfile, updateProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', getProfile, name='get_profile'),
    path('profile/update/', updateProfile, name='update_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


# Endpoints
    path('api/components/components', include('components.endpoints.component')),
    path('api/components/component_types', include('components.endpoints.component_type')),
    path('api/contacts/contact_businesses', include('contacts.endpoints.contact_business')),
    path('api/contacts/contacts', include('contacts.endpoints.contact')),
    path('api/contacts/contact_categories', include('contacts.endpoints.contact_category')),
    path('api/customers/customer', include('customers.endpoints.customer')),
    path('api/customers/agent', include('customers.endpoints.agent')),
    path('api/db_changes', include('db_changes.endpoints.db_changes')),

    path('api/hotels', include('hotels.endpoints.hotels')),
    path('api/hotels/agent_hotels', include('hotels.endpoints.agent_hotels')),
    path('api/hotels/customized_hotels', include('hotels.endpoints.customized_hotels')),
    path('api/hotels/hotel_rooms', include('hotels.endpoints.hotel_rooms')),
    path('api/hotels/room_prices', include('hotels.endpoints.room_prices')),

    path('api/media/photos', include('media.endpoints.photos')),
    path('api/media/videos', include('media.endpoints.videos')),
    # THERE IS ALSO A api/media/photos/unverified and the same for videos

    path('api/regions', include('region.endpoints.regions')),
    path('api/reviews', include('reviews.endpoints.review')),
    path('api/waypoints', include('waypoints.endpoints.waypoints')),


    path('api/itineraries/agent_itineraries', include('itineraries.endpoints.agent_itinerary')),
    path('api/itineraries/customer_itineraries', include('itineraries.endpoints.customer_itinerary')),
    path('api/itineraries/itinerary_day_components', include('itineraries.endpoints.itinerary_day_component')),
    path('api/itineraries/itinerary_days', include('itineraries.endpoints.itinerary_day')),
    path('api/itineraries/itinerary.groups', include('itineraries.endpoints.itinerary_group')),
    path('api/itineraries/itinerary.groupings', include('itineraries.endpoints.itinerary_grouping')),


    path('', include('frontend.urls')),
    re_path(r'^(?:.*)?', include('frontend.urls'))

]
