from collections import UserList
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from core.pagination import CustomPageNumberPagination
from users.models import User, Userlist
from .permissions import HasPermission, HasToken
from animes.models import Anime
from rest_framework.authentication import TokenAuthentication
from userslist.serializers import UserListSerializer


def formatted_response(data):

    serializer_data = {
        **data,
        "anime": {
            "id": Anime.objects.get(pk=data["anime"]).id,
            "title": Anime.objects.get(pk=data["anime"]).title,
            "image": Anime.objects.get(pk=data["anime"]).image,
            "average_rate": Anime.objects.get(pk=data["anime"]).average_rate,
        },
        "user": {
            "id": User.objects.get(pk=data["user"]).id,
            "name": User.objects.get(pk=data["user"]).first_name,
        },
    }

    return serializer_data


class UserlistView(APIView, CustomPageNumberPagination):

    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken, HasPermission]

    def get(self, request):

        userlist = Userlist.objects.filter(user=request.user)
        result_page = self.paginate_queryset(userlist, request, view=self)
        serializer = UserListSerializer(result_page, many=True)
        serializer_data = []

        for values in serializer.data:
            serializer_data.append(formatted_response(values))

        return self.get_paginated_response(serializer_data)


class UserlistViewDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]

    def post(self, request: Request, anime_id):

        anime = get_object_or_404(Anime, pk=anime_id)
        serializer = UserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, anime=anime)
        serializer_data = formatted_response(serializer.data)
        return Response(serializer_data, status.HTTP_201_CREATED)

    def patch(self, request: Request, myanime_id):

        my_anime = get_object_or_404(Userlist, pk=myanime_id)
        serializer = UserListSerializer(instance=my_anime, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_data = formatted_response(serializer.data)
        return Response(serializer_data, status.HTTP_200_OK)
