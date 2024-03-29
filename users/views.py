from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, UserUpdateSerializer
from users.permissions import UserPermission, AdminPermission
from users.mixins import SerializerByMethodMixin


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(APIView):
    def post(self, req: Request):
        serialized = LoginSerializer(data=req.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, req: Request):
        user: User = req.user
        serialized = UserSerializer(instance=user)

        return Response(serialized.data, status.HTTP_200_OK)

    def patch(self, req: Request):
        user: User = req.user

        serialized = UserUpdateSerializer(instance=user, data=req.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        serialized = UserSerializer(instance=serialized.instance)

        if req.data.get("password"):
            token, _ = Token.objects.get_or_create(user=user)
            token.delete()

        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, req: Request):
        user: User = req.user
        user.delete()

        return Response("", status.HTTP_204_NO_CONTENT)


class AdminView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminIdView(SerializerByMethodMixin, generics.RetrieveAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    
    queryset = User.objects.all()
    serializer_map = {
        "GET": UserSerializer,
        "DELETE": UserSerializer
    }
