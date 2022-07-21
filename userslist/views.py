from collections import UserList
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from core.pagination import CustomPageNumberPagination
from users.models import Userlist
from .permissions import HasPermission
from animes.models import Anime
from rest_framework.authentication import TokenAuthentication
from userslist.serializers import UserListSerializer


class UserlistView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]

    def get(self, request):

        userlist = Userlist.objects.all()
        result_page = self.paginate_queryset(userlist, request, view=self)
        serializer = UserListSerializer(result_page, many=True)
        serializer_data = []

        for values in serializer.data:
            serializer_data.append(values)

        return self.get_paginated_response(serializer_data)

class UserlistViewDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]
    
    def post(self, request: Request, anime_id):
        
        anime = get_object_or_404(Anime, pk=anime_id)
        serializer = UserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, anime=anime)
        serializer_data = serializer.data
        return Response(serializer_data, status.HTTP_201_CREATED)

    def patch(self, request: Request, anime_id):

        anime = get_object_or_404(Anime, pk=anime_id)
        serializer = UserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, anime=anime)
        serializer_data = serializer.data
        return Response(serializer_data, status.HTTP_200_OK)