from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Agent, Customer
from .serializers import AgentSerializer, CustomerSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin

User = get_user_model()  # Get the custom user model

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        # Only allow admin users to update the admin_description field
        if 'admin_description' in request.data and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to update this field.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Only allow admin users to update the admin_description field
        if 'admin_description' in request.data and not request.user.is_staff:
            return Response({'detail': 'You do not have permission to update this field.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Customer.objects.none()
        return Customer.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Retrieve or update the current user's data.
    """
    user = request.user
    if isinstance(user, Agent):
        serializer_class = AgentSerializer
    elif isinstance(user, Customer):
        serializer_class = CustomerSerializer
    else:
        return Response({"error": "User type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = serializer_class(user)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = serializer_class(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    """
    Update the current user's profile.
    """
    user = request.user
    if isinstance(user, Agent):
        serializer_class = AgentSerializer
    elif isinstance(user, Customer):
        serializer_class = CustomerSerializer
    else:
        return Response({"error": "User type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer_class(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    """
    Retrieve the profile of the current user.
    """
    user = request.user
    if hasattr(user, 'agent'):
        serializer_class = AgentSerializer
    elif hasattr(user, 'customer'):
        serializer_class = CustomerSerializer
    else:
        return Response({"error": "User type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = serializer_class(user)
    return Response(serializer.data)
