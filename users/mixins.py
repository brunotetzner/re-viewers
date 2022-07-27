from rest_framework.views import Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from users.serializers import LoginSerializer


class SerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)


class LoginModelMixins:
    def login(self, request, *args, **kwargs):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user = authenticate(**serialized.validated_data)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED
            )
            
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)
