from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer

# Create your views here.


class RegisterUserView(APIView):
    class RegisterUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                "id",
                "username",
                "email",
                "password",
                "first_name",
                "last_name"
            )

    def post(self, request):
        serializer = self.RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response(UserSerializer(user).data, status=201)


class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
