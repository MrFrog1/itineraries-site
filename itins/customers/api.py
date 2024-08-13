from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import LoginUserSerializer, UserSerializer, CustomerRegisterSerializer, AgentProfileSerializer, PotentialAgentSerializer, PotentialAgentListSerializer
from .permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin
from oauth2_provider.models import Application
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from .models import PotentialAgent, UserAgent
from .serializers import AgentRegisterSerializer, PotentialAgentSerializer, PotentialAgentListSerializer    
from django.db.models import Q
from rest_framework.permissions import AllowAny
from django.views.decorators.debug import sensitive_post_parameters
import json

from oauthlib.oauth2 import OAuth2Error
import logging


logger = logging.getLogger(__name__)

UserModel = get_user_model()  # Get the custom user model

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return UserModel.objects.all().select_related('user_agent', 'customer_profile')
        
        visible_users = UserModel.objects.filter(public_profile=True).select_related('user_agent', 'customer_profile')
        
        if user.is_agent:
            interacted_customers = UserModel.objects.filter(
                is_customer=True, 
                customer_profile__interacted_agents=user
            ).exclude(
                customer_profile__blocked_agents=user
            ).select_related('customer_profile')
            visible_users = visible_users | interacted_customers

        return visible_users.distinct()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Check if the user is trying to update sensitive fields
        sensitive_fields = ['default_commission_percentage', 'default_organisation_fee']
        for field in sensitive_fields:
            if field in serializer.validated_data and not request.user.is_superuser:
                if instance != request.user:
                    return Response({"detail": "You don't have permission to update this field."},
                                    status=status.HTTP_403_FORBIDDEN)
        
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.instance
        user_agent_data = serializer.validated_data.pop('user_agent', None)
        
        serializer.save()
        
        if user_agent_data and instance.is_agent:
            user_agent = instance.user_agent
            for attr, value in user_agent_data.items():
                setattr(user_agent, attr, value)
            user_agent.save()

# Authentication related

class TokenView(OAuthLibMixin, APIView):
    permission_classes = []
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def create_token_response(self, request):
        if 'grant_type' not in request.POST:
            raise OAuthToolkitError('The grant type is mandatory')

        grant_type = request.POST.get('grant_type')

        if grant_type not in ['password', 'refresh_token', 'authorization_code', 'client_credentials']:
            raise OAuthToolkitError('Unsupported grant type')

        if 'client_id' not in request.POST:
            if grant_type == 'password':
                # Only use default application for password grant
                application = Application.objects.get(name="Default")
                request.POST = request.POST.copy()
                request.POST['client_id'] = application.client_id
                request.POST['client_secret'] = application.client_secret
            else:
                raise OAuth2Error('Client credentials are mandatory')

        # Handle email/username
        if grant_type == 'password':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if '@' in username:
                try:
                    user = UserModel.objects.get(email=username)
                    username = user.username
                except UserModel.DoesNotExist:
                    pass

            user = authenticate(username=username, password=password)
            if user:
                request.user = user
            else:
                print(f"Authentication failed for username: {username}")

        return super().create_token_response(request)

    def post(self, request, *args, **kwargs):
        
        try:
            url, headers, body, status = self.create_token_response(request)
            response_data = json.loads(body)
            
            
            if status == 200:
                user = request.user

                
                user_data = LoginUserSerializer(user).data
                response_data.update(user_data)
            else:
                print(f"Token creation failed. Status: {status}, Response: {response_data}")
            
            
            response = Response(data=response_data, status=status)

            for k, v in headers.items():
                response[k] = v

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class CustomerRegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Create an OAuth2 application for this user
        Application.objects.create(
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Retrieve or update the current user's data.
    """
    user = request.user
    serializer = UserSerializer(user, context={'request': request})

    if request.method == 'GET':
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentRegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AgentRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_agent=True, is_customer=False)
        # Create an OAuth2 application for this user
        Application.objects.create(
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            name=f"{user.username}'s application"
        )
    
# AGENT LOGIC


class AgentProfileView(RetrieveAPIView):
    queryset = UserAgent.objects.all
    serializer_class = AgentProfileSerializer


class CreateAgentView(generics.CreateAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = [permissions.IsAdminUser]  # Adjust as needed

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Add any additional logic for agent creation
        serializer.save(is_agent=True)


class AllAgentsView(generics.ListAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = UserAgent.objects.all()
        if not self.request.user.is_authenticated or self.request.user.is_customer:
            queryset = queryset.filter(user__public_profile=True)
        return queryset.select_related('user').prefetch_related('expertise_categories')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Returning {len(serializer.data)} agents")
        return Response(serializer.data)


# This AgentSearchView gives the option to include potential agents in the search - non-uiser agents, or just agents or both
class AgentSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.query_params.get('include_potential', 'false').lower() == 'true':
            return PotentialAgentListSerializer
        return AgentProfileSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('q', None)
        include_potential = self.request.query_params.get('include_potential', 'false').lower() == 'true'
        
        user_agent_queryset = UserAgent.objects.all()
        potential_agent_queryset = PotentialAgent.objects.all() if include_potential else PotentialAgent.objects.none()

        if search_term:
            user_agent_queryset = user_agent_queryset.filter(
                Q(user__username__icontains=search_term) |
                Q(user__email__icontains=search_term) |
                Q(user__first_name__icontains=search_term) |
                Q(user__last_name__icontains=search_term) |
                Q(user__nickname__icontains=search_term) |
                Q(business_name__icontains=search_term) |
                Q(short_bio__icontains=search_term) |
                Q(bio__icontains=search_term) |
                Q(expertise_categories__name__icontains=search_term)
            ).distinct()

            if include_potential:
                potential_agent_queryset = potential_agent_queryset.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(email__icontains=search_term) |
                    Q(business_name__icontains=search_term) |
                    Q(short_bio__icontains=search_term) |
                    Q(bio__icontains=search_term) |
                    Q(expertise_categories__name__icontains=search_term)
                ).distinct()

        if not self.request.user.is_authenticated or self.request.user.is_customer:
            user_agent_queryset = user_agent_queryset.filter(user__public_profile=True)

        # Combine the querysets
        combined_queryset = list(user_agent_queryset) + list(potential_agent_queryset)
        return combined_queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['search_results'] = True
        return context

# Potential Agent Logic

class AllPotentialAgentsView(generics.ListAPIView):
    serializer_class = PotentialAgentListSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can view potential agents

    def get_queryset(self):
        return PotentialAgent.objects.all().prefetch_related('expertise_categories')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Returning {len(serializer.data)} potential agents")
        return Response(serializer.data)
    

class CreatePotentialAgentView(generics.CreateAPIView):
    queryset = PotentialAgent.objects.all()
    serializer_class = PotentialAgentSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

