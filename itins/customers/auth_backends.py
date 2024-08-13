from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken

UserModel = get_user_model()

class OAuth2Backend(ModelBackend):
    def authenticate(self, request, token=None, **kwargs):
        if token:
            try:
                access_token = AccessToken.objects.get(token=token)
                return access_token.user
            except AccessToken.DoesNotExist:
                return None
        return super().authenticate(request, **kwargs)