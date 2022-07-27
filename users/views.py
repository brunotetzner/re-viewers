from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, UserUpdateSerializer
from users.permissions import UserPermission, AdminPermission
from users.mixins import SerializerByMethodMixin, LoginModelMixins


class UserRegisterView(SerializerByMethodMixin, generics.CreateAPIView):
    serializer_map = {
        "POST": UserSerializer
    }


class UserLoginView(LoginModelMixins, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.login(request, *args, **kwargs)


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


class AdminView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]

    def get(self, _: Request):
        users = User.objects.all()
        serialized = UserSerializer(instance=users, many=True)

        return Response(serialized.data, status.HTTP_200_OK)


class AdminIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]

    def get(self, _: Request, id: str):
        user: User = get_object_or_404(User, pk=id)
        serialized = UserSerializer(instance=user)

        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, _: Request, id: str):
        user: User = get_object_or_404(User, pk=id)
        user.delete()

        return Response("", status.HTTP_200_OK)
