from django.db import models
from itineraries.models import CustomerItinerary, AgentItinerary, ItineraryDay, ItineraryGroup
from contacts.models import Contact
from region.models import Region
from components.models import Component
from hotels.models import Hotel, HotelActivities
from reviews.models import Review
from django.conf import settings
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Custom validator for file size
def validate_file_size(file):
    max_size_mb = 5  # Max size in MB for photos
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Maximum file size is {max_size_mb}MB")


# Create your models here.

class Photo(models.Model):

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_by_admin = models.BooleanField(default=False)
    is_agent_bio_photo = models.BooleanField(default=False)

    verified_by_admin = models.BooleanField(null=True)

    # Many-to-many relationships to allow multiple associations
    customer_itineraries = models.ManyToManyField(CustomerItinerary, blank=True)
    agent_itineraries = models.ManyToManyField(AgentItinerary, blank=True)
    itinerary_days = models.ManyToManyField(ItineraryDay, blank=True)
    itinerary_groups = models.ManyToManyField(ItineraryGroup, blank=True)
    primary_photo = models.BooleanField(default=False)

    image = models.ImageField(
        upload_to='photos/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_file_size]
    )
    image_thumbnail = models.ImageField(upload_to='photos/thumbnails/', null=True, blank=True)
    image_medium = models.ImageField(upload_to='photos/medium/', null=True, blank=True)
    image_full = models.ImageField(upload_to='photos/full/', null=True, blank=True)
    primary_image = models.BooleanField(default=False)

    upload_date = models.DateTimeField(auto_now_add=True) 
    image_size = models.PositiveIntegerField(null=True, blank=True)  # You can populate this field during file upload

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, null=True, blank=True)

    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True, null=True)  # Assuming null is allowed
    hotel_activity = models.ForeignKey(HotelActivities, on_delete=models.CASCADE, blank=True, null=True)  # Assuming null is allowed


    def clean(self):
        if self.uploader.is_superuser or self.uploader.is_staff:
            # Admins can upload photos without restrictions
            return

        if self.uploader.is_customer:
            if not self.review:
                raise ValidationError("Customers can only upload photos with reviews.")
        
        elif self.uploader.is_agent:
            if self.id is None:  # This is a new, unsaved Photo
                if not (self.hotel or self.hotel_activity or self.contact or self.itinerary_day or self.itinerary_group):
                    raise ValidationError("Agents can only upload photos for their hotels, hotel activities, contacts, itinerary days, or itinerary groups.")
            else:  # This is an existing Photo
                if not (self.hotel or self.hotel_activity or self.agent_itineraries.exists() or self.contact or self.itinerary_day or self.itinerary_group):
                    raise ValidationError("Agents can only upload photos for their hotels, hotel activities, itineraries, contacts, itinerary days, or itinerary groups.")
            
            # Additional checks to ensure the agent owns the related objects
            if self.hotel and self.hotel.agent != self.uploader:
                raise ValidationError("Agents can only upload photos for their own hotels.")
            if self.hotel_activity and self.hotel_activity.agent != self.uploader:
                raise ValidationError("Agents can only upload photos for their own hotel activities.")
            if self.contact and self.contact.agent != self.uploader:
                raise ValidationError("Agents can only upload photos for their own contacts.")
            if self.itinerary_day and self.itinerary_day.itinerary_group.agent_itinerary.agent != self.uploader:
                raise ValidationError("Agents can only upload photos for their own itinerary days.")
            if self.itinerary_group and self.itinerary_group.agent_itinerary.agent != self.uploader:
                raise ValidationError("Agents can only upload photos for their own itinerary groups.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=['uploader', 'verified_by_admin']),
            models.Index(fields=['region']),
            models.Index(fields=['hotel']),
        ]


    def get_cached_image_url(self):
        cache_key = f"photo_url_{self.id}"
        try:
            cached_url = cache.get(cache_key)
            if cached_url is None:
                if self.image and self.image.name:
                    cached_url = self.image.url
                    cache.set(cache_key, cached_url, settings.CACHE_TTL)
                else:
                    logger.warning(f"No image associated with Photo ID: {self.id}")
                    return None
            return cached_url
        except Exception as e:
            logger.exception(f"Error getting cached image URL for Photo ID {self.id}: {str(e)}")
            return None
    
# Custom validator for video size
def validate_video_size(file):
    max_size_mb = 50  # Max size in MB for videos   
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Maximum file size is {max_size_mb}MB")


class Video(models.Model):

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_agent_bio_video = models.BooleanField(default=False)

    verified_by_admin = models.BooleanField(null=True)
    customer_itineraries = models.ManyToManyField(CustomerItinerary, blank=True)
    agent_itineraries = models.ManyToManyField(AgentItinerary, blank=True)

    video = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov']), validate_video_size]
    )  
    upload_date = models.DateTimeField(auto_now_add=True)
    video_duration = models.DurationField()  # Populate this field based on the video file

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, blank=True, null=True)  # Assuming null is allowed
    description = models.CharField(max_length=150)

