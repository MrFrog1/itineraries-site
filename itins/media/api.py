
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Photo, Video
from .serializers import BasicPhotoSerializer, DetailedPhotoSerializer, VideoSerializer
from .permissions import IsUploaderOrReadOnly
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
import logging


logger = logging.getLogger(__name__)

class PhotoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUploaderOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'hotel', 'agent_itineraries', 'customer_itineraries', 'primary_image', 'is_agent_bio_photo']
    search_fields = ['region__name', 'category', 'description']
    ordering_fields = ['upload_date', 'image_size']
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        queryset = Photo.objects.all()
        user = self.request.user

        # Filter based on the foreign key instance provided in the query params
        filter_params = {
            'customer_itinerary_id': 'customer_itineraries__id',
            'agent_itinerary_id': 'agent_itineraries__id',
            'itinerary_day_id': 'itinerary_days__id',
            'itinerary_group_id': 'itinerary_groups__id',
            'region_id': 'region__id',
            'contact_id': 'contact__id',
            'review_id': 'review__id',
            'hotel_id': 'hotel__id',
            'hotel_activity_id': 'hotel_activity__id',
        }

        for param, field in filter_params.items():
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{field: value})

        # Filter based on the photo type (primary or agent bio)
        primary_photo = self.request.query_params.get('primary_photo')
        agent_bio_photo = self.request.query_params.get('agent_bio_photo')

        if primary_photo:
            queryset = queryset.filter(primary_image=True)
        elif agent_bio_photo:
            queryset = queryset.filter(is_agent_bio_photo=True)

        if user.is_staff:
            final_queryset = queryset
        elif user.is_authenticated:
            final_queryset = queryset.filter(Q(verified_by_admin=True) | Q(uploader=user) | Q(verified_by_admin__isnull=True, uploader=user))
        else:
            final_queryset = queryset.filter(verified_by_admin=True)

        logger.debug(f"Filtered queryset: {final_queryset.query}")
        return final_queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BasicPhotoSerializer
        return DetailedPhotoSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        logger.info(f"Received photo upload request. Data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
                logger.info(f"Photo created successfully. ID: {instance.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.exception(f"Error creating photo: {str(e)}")
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Photo creation failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Photo instance created. ID: {instance.id}, Image: {instance.image.name if instance.image else 'No image'}")
        
    @action(detail=False, methods=['get'])
    def primary(self, request):
        primary_photos = self.get_queryset().filter(primary_image=True)
        serializer = BasicPhotoSerializer(primary_photos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_foreign_key(self, request):
        queryset = self.get_queryset()
        serializer = BasicPhotoSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def unverified(self, request):
        queryset = self.get_queryset().filter(verified_by_admin__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsUploaderOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['region__name', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Video.objects.all()
        elif user.is_authenticated:
            return Video.objects.filter(Q(verified_by_admin=True) | Q(uploader=user) | Q(verified_by_admin__isnull=True, uploader=user))
        else:
            return Video.objects.filter(verified_by_admin=True)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def unverified(self, request):
        queryset = self.get_queryset().filter(verified_by_admin__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)