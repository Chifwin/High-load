import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header or len(auth_header) != 2:
            return None
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")
        if prefix.lower() != auth_header_prefix:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            raise exceptions.AuthenticationFailed("Cannot decode token")
        try:
            user = User.objects.get(id=payload["id"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No user with token.")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is deactivated.")
        return user, token
