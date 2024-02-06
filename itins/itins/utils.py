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
