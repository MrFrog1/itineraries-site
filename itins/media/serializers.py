from rest_framework import serializers
from .models import Photo, Video
from PIL import Image
from io import BytesIO
import logging
from django.contrib.auth import get_user_model

User = get_user_model()


logger = logging.getLogger(__name__)


class BasicPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['id', 'image_thumbnail', 'primary_image', 'category']

    def get_image_url(self, obj):
        return obj.get_cached_image_url()
        
class DetailedPhotoSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')
    crop_data = serializers.JSONField(required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ['itinerary_days', 'itinerary_groups', 'customer_itineraries', 'agent_itineraries', 'region', 'contact', 'review', 'hotel', 'component', 'uploaded_by_admin']
    def validate(self, data):
        user = self.context['request'].user
        
        if user.is_superuser or user.is_staff:
            return data
        
        if user.is_customer and not data.get('review'):
            raise serializers.ValidationError("Customers can only upload photos with reviews.")
        
        if user.is_agent:
            if not (data.get('hotel') or data.get('hotel_activity') or data.get('contact') or 
                    data.get('itinerary_day') or data.get('itinerary_group')):
                raise serializers.ValidationError("Agents can only upload photos for their hotels, hotel activities, contacts, itinerary days, or itinerary groups.")
            
            # Additional checks to ensure the agent owns the related objects
            if data.get('hotel') and data['hotel'].agent != user:
                raise serializers.ValidationError("Agents can only upload photos for their own hotels.")
            if data.get('hotel_activity') and data['hotel_activity'].agent != user:
                raise serializers.ValidationError("Agents can only upload photos for their own hotel activities.")
            if data.get('contact') and data['contact'].agent != user:
                raise serializers.ValidationError("Agents can only upload photos for their own contacts.")
            if data.get('itinerary_day') and data['itinerary_day'].itinerary_group.agent_itinerary.agent != user:
                raise serializers.ValidationError("Agents can only upload photos for their own itinerary days.")
            if data.get('itinerary_group') and data['itinerary_group'].agent_itinerary.agent != user:
                raise serializers.ValidationError("Agents can only upload photos for their own itinerary groups.")
        
    def create(self, validated_data):
        logger.info(f"Creating photo with data: {validated_data}")
        user = self.context['request'].user
        
        # Handle admin uploading for an agent
        if (user.is_staff or user.is_superuser) and 'agent_id' in self.context['request'].data:
            agent_id = self.context['request'].data['agent_id']
            try:
                agent = User.objects.get(id=agent_id, is_agent=True)
                validated_data['uploader'] = agent
            except User.DoesNotExist:
                raise serializers.ValidationError("Specified agent does not exist.")
        else:
            validated_data['uploader'] = user
        
        if user.is_staff or user.is_superuser:
            validated_data['uploaded_by_admin'] = True
        
        image_file = validated_data.pop('image', None)
        if not image_file:
            raise serializers.ValidationError("No image file provided")

        crop_data = validated_data.pop('crop_data', None)

        try:
            photo = Photo(**validated_data)
            photo.image.save(image_file.name, image_file, save=False)
            logger.info(f"Original image saved: {photo.image.name}")

            # Optimize and save other versions
            optimized_images = self.optimize_image(photo.image, crop_data)

            photo.image_thumbnail.save(f"{photo.id}_thumbnail.jpg", optimized_images['thumbnail'], save=False)
            photo.image_medium.save(f"{photo.id}_medium.jpg", optimized_images['medium'], save=False)
            photo.image_full.save(f"{photo.id}_full.jpg", optimized_images['full'], save=False)

            photo.save()
            logger.info(f"Photo saved successfully with all image versions. ID: {photo.id}")

            return photo
        except Exception as e:
            logger.exception(f"Error creating photo: {str(e)}")
            if photo.id:
                photo.delete()
            raise serializers.ValidationError(f"Error creating photo: {str(e)}")

    def optimize_image(self, image_file, crop_data=None):
        logger.info("Optimizing image")

        # Open the uploaded image
        image = Image.open(image_file)

        # Crop the image if crop data is provided
        if crop_data:
            left = crop_data['left']
            top = crop_data['top']
            right = crop_data['right']
            bottom = crop_data['bottom']
            image = image.crop((left, top, right, bottom))

        # Determine the appropriate dimensions based on usage
        thumbnail_size = (300, 300)
        medium_size = (800, 800)
        full_size = (1600, 1600)

        # Create optimized versions of the image
        thumbnail = self.resize_image(image, thumbnail_size)
        medium = self.resize_image(image, medium_size)
        full = self.resize_image(image, full_size)

        # Compress the images
        thumbnail_compressed = self.compress_image(thumbnail, 'JPEG', 80)
        medium_compressed = self.compress_image(medium, 'JPEG', 85)
        full_compressed = self.compress_image(full, 'JPEG', 90)

        return {
            'thumbnail': thumbnail_compressed,
            'medium': medium_compressed,
            'full': full_compressed
        }

    def resize_image(self, image, size):
        # Resize the image while maintaining the aspect ratio
        image.thumbnail(size)
        return image

    def compress_image(self, image, format, quality):
        # Compress the image
        compressed_image = BytesIO()
        image.save(compressed_image, format, optimize=True, quality=quality)
        compressed_image.seek(0)
        return compressed_image

    def get_image_url(self, obj):
        return obj.get_cached_image_url()
    
class VideoSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['customer_itineraries', 'agent_itineraries', 'region', 'hotel']  


