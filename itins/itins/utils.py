from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


def custom_jwt_response_handler(token, user=None, request=None):
    """
    Custom JWT response payload handler.
    """
    # Defer the import to avoid 'AppRegistryNotReady' error
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    response_data = {
        'refresh': str(refresh),
        'access': str(token),
        'user': {
            'username': user.username,
            'email': user.email,
            # Add more fields as needed
        }
    }
    return response_data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer to modify the token response.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        # Call the custom response handler here
        data.update(custom_jwt_response_handler(self.get_token(self.user), self.user))
        return data
    

# itins/utils.py (continue from the previous code)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView to use the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer
