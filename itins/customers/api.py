from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, MyTokenObtainPairSerializer, CustomerRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from django.conf import settings


UserModel = get_user_model()  # Get the custom user model

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Simplified for demonstration; adjust according to your permission requirements
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def update(self, request, *args, **kwargs):
        # Custom update logic if needed
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Custom partial_update logic if needed
        return super().partial_update(request, *args, **kwargs)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        refresh_token = data.pop('refresh', None)
        
        if refresh_token:
            cookie_max_age = 3600 * 24 * 3  # 3 days
            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=cookie_max_age,
                httponly=True,
                samesite='Strict',
                secure=not settings.DEBUG  # Set to True in production
            )
        return response

class CustomerRegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerRegisterSerializer
 
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
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
