from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import LoginUserSerializer, UserSerializer, CustomerRegisterSerializer, AgentProfileSerializer
from .permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin
from oauth2_provider.models import Application
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from .serializers import AgentRegisterSerializer
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
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return UserModel.objects.all()
        
        visible_users = UserModel.objects.filter(public_profile=True)
        
        if user.is_agent:
            # Include customers who have interacted with this agent
            interacted_customers = UserModel.objects.filter(
                is_customer=True, 
                customer_profile__interacted_agents=user
            ).exclude(
                customer_profile__blocked_agents=user
            )
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
    
class AgentProfileView(RetrieveAPIView):
    queryset = UserModel.objects.filter(is_agent=True)
    serializer_class = UserSerializer

class AllAgentsView(generics.ListAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = UserModel.objects.filter(is_agent=True)

        if not self.request.user.is_authenticated or self.request.user.is_customer:
            queryset = queryset.filter(public_profile=True)

        return queryset.select_related('agent_profile').prefetch_related('agent_profile__expertise_categories')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Returning {len(serializer.data)} agents")
        return Response(serializer.data)


class AgentSearchView(generics.ListAPIView):
    serializer_class = AgentProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = UserModel.objects.filter(is_agent=True)
        search_term = self.request.query_params.get('q', None)
        
        logger.info(f"Searching for term: {search_term}")

        if search_term:
            queryset = queryset.filter(
                Q(username__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(nickname__icontains=search_term) |
                Q(agent_profile__business_name__icontains=search_term) |
                Q(agent_profile__short_bio__icontains=search_term) |
                Q(agent_profile__bio__icontains=search_term) |
                Q(agent_profile__expertise_categories__name__icontains=search_term)
            ).distinct()

        if not self.request.user.is_authenticated or self.request.user.is_customer:
            queryset = queryset.filter(public_profile=True)

        logger.info(f"Query returned {queryset.count()} results")

        return queryset.select_related('agent_profile').prefetch_related('agent_profile__expertise_categories')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            logger.info(f"Returning {len(serializer.data)} results")
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Returning {len(serializer.data)} results")
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['search_results'] = True
        return context