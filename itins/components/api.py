from django.db import models
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Component, ComponentType
from .serializers import ComponentSerializer, ComponentTypeSerializer
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admin users can see all components
            return Component.objects.all()
        elif hasattr(user, 'agent'):
            # Agents can only see their components
            return Component.objects.filter(agent=user.agent)
        else:
            # Other users should not see any components
            return Component.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(agent=self.request.user.agent)
        else:
            serializer.save()


    def perform_update(self, serializer):
        component = serializer.instance
        if self.request.user.is_superuser or component.agent == self.request.user.agent:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to edit this component.")

    def destroy(self, request, *args, **kwargs):
        try:
            component = self.get_object()
        except Component.DoesNotExist:
            raise NotFound("The requested component does not exist.")

        if request.user.is_superuser or component.agent == request.user.agent:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to delete this component.")

    # Optionally, you can override handle_exception to customize error responses
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        elif isinstance(exc, NotFound):
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        # Default exception handling
        return super(ComponentViewSet, self).handle_exception(exc)
    

    
class ComponentTypeViewSet(viewsets.ModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent)

    def get_queryset(self):
        # This will return global types and types created by the logged-in agent
        return ComponentType.objects.filter(
            models.Q(agent__isnull=True) | models.Q(agent=self.request.user.agent)
        )