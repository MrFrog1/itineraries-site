from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contact, ContactBusiness, ContactCategory
from .serializers import ContactSerializer, ContactBusinessSerializer, ContactCategorySerializer
from .permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Contact.objects.all()
        elif user.is_authenticated:
            return Contact.objects.filter(
                Q(agent=user) | Q(is_visible_to_others=True)
            )
        else:
            return Contact.objects.filter(is_visible_to_others=True)

    def perform_create(self, serializer):
        agent_id = self.request.data.get('agent')
        if agent_id:
            try:
                agent = User.objects.get(id=agent_id)
            except User.DoesNotExist:
                agent = self.request.user
        else:
            agent = self.request.user
        
        serializer.save(agent=agent)

class ContactCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ContactCategorySerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ContactCategory.objects.filter(agent=user)
        return ContactCategory.objects.none()

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

    @action(detail=False, methods=['POST'])
    def create_default_categories(self, request):
        ContactCategory.create_default_categories(request.user)
        return Response({"status": "Default categories created"}, status=status.HTTP_201_CREATED)

class ContactBusinessViewSet(viewsets.ModelViewSet):
    serializer_class = ContactBusinessSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ContactBusiness.objects.filter(agent=user)
        return ContactBusiness.objects.none()

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)