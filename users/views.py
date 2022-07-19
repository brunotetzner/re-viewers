from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, UserUpdateSerializer


class UserRegisterView(APIView):
    def post(self, req: Request):
        serialized = UserSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        
        return Response(serialized.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, req: Request):
        serialized = LoginSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)
        
        user: User = authenticate(**serialized.validated_data)
        if not user:
            return Response({ "error": "Invalid credentials" }, status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({ "token": token.key })
