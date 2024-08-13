from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django.db.models import Q

from .models import Component, ComponentType
from .serializers import ComponentSerializer, ComponentTypeSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class ComponentFilter(FilterSet):
    class Meta:
        model = Component
        fields = ['component_type', 'fitness_level', 'is_platform_experience']

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ComponentFilter


    def get_queryset(self):
        queryset = Component.objects.all()
        print('first step')
        agent_id = self.request.query_params.get('agent_id', None)
        print(agent_id)
        if agent_id is not None:
            queryset = queryset.filter(agent_id=agent_id)
            print(queryset)
        return queryset
# Allows for filtering to see ones visible to all - admin and public components


    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)


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

    @action(detail=True, methods=['post'])
    def transfer_to_agent(self, request, pk=None):
        component = self.get_object()
        new_agent_id = request.data.get('new_agent_id')
        
        try:
            new_agent = User.objects.get(id=new_agent_id)
        except User.DoesNotExist:
            return Response({'error': 'Agent not found'}, status=status.HTTP_400_BAD_REQUEST)

        new_component = self.get_serializer().transfer_to_agent(component, new_agent)
        return Response(self.get_serializer(new_component).data)

    @action(detail=False, methods=['post'])
    def create_for_agents(self, request):
        agent_ids = request.data.pop('agent_ids', [])
        agents = User.objects.filter(id__in=agent_ids)
        
        if not agents:
            return Response({'error': 'No valid agents provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_components = self.get_serializer.create_for_agents(agents, serializer.validated_data)
        return Response(self.get_serializer(new_components, many=True).data)
    


class ComponentTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ComponentTypeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['agent', 'is_global']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        agent_id = self.request.query_params.get('agent_id')
        
        if agent_id:
            # If an agent_id is provided, return ComponentTypes for that agent and global types created by admin
            return ComponentType.objects.filter(
                Q(agent_id=agent_id) | 
                Q(is_global=True, agent__is_superuser=True)
            )
        elif user.is_staff:
            # If no agent_id is provided and the user is staff, return all ComponentTypes
            return ComponentType.objects.all()
        else:
            # If no agent_id is provided and the user is not staff, return global types and types belonging to the current user
            return ComponentType.objects.filter(
                Q(is_global=True) | 
                Q(agent=user)
            )

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