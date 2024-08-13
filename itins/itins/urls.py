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
from customers.api import CustomerRegisterView, current_user, AgentProfileView, AllAgentsView, TokenView, AgentRegisterView, AgentSearchView
from region.api import RegionViewSet
from django.conf import settings
from django.conf.urls.static import static
from oauth2_provider.urls import base_urlpatterns, app_name
from oauth2_provider.views import AuthorizationView, TokenView as OAuthTokenView, RevokeTokenView


oauth2_endpoint_views = [
    path('authorize/', AuthorizationView.as_view(), name="authorize"),
    path('token/', TokenView.as_view(), name="token"),
    path('revoke_token/', RevokeTokenView.as_view(), name="revoke-token"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),


# Registering/Creation

    path('register/', CustomerRegisterView.as_view(), name='register'),
    path('register/agent/', AgentRegisterView.as_view(), name='agent_register'),


    path('profile/', current_user, name='current_user'),

# Agents 
    path('api/agents/<int:pk>/', AgentProfileView.as_view(), name='agent-profile'),
    path('api/agents/search/', AgentSearchView.as_view(), name='agent-search'),
    path('api/agents/', AllAgentsView.as_view(), name='all-agents'),


# Endpoints
    path('api/components/components', include('components.endpoints.component')),
    path('api/components/component_types', include('components.endpoints.component_type')),
    path('api/contacts/contact_businesses', include('contacts.endpoints.contact_business')),
    path('api/contacts/contacts', include('contacts.endpoints.contact')),
    path('api/contacts/contact_categories', include('contacts.endpoints.contact_category')),
    path('api/user', include('customers.endpoints.user')),
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
    path('api/regions/detailed', RegionViewSet.as_view({'post': 'detailed'}), name='regions-detailed'),
    path('api/reviews', include('reviews.endpoints.review')),
    path('api/waypoints', include('waypoints.endpoints.waypoints')),
    path('api/airports/', include('waypoints.endpoints.airports')),

    # path('api/search', include('search.endpoints.search')),

    path('api/airports/', include('waypoints.endpoints.airports')),

    path('api/itineraries/', include('itineraries.endpoints.agent_itinerary')),
    path('api/itineraries/customer_itineraries', include('itineraries.endpoints.customer_itinerary')),
    path('api/itineraries/itinerary_day_components', include('itineraries.endpoints.itinerary_day_component')),
    path('api/itineraries/itinerary_days', include('itineraries.endpoints.itinerary_day')),
    path('api/itineraries/itinerary.groups', include('itineraries.endpoints.itinerary_group')),
    path('api/itineraries/itinerary.groupings', include('itineraries.endpoints.itinerary_grouping')),


    # path('', include('frontend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)