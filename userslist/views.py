from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from core.pagination import CustomPageNumberPagination
from users.models import Userlist
from animes.models import Anime

from userslist.serializers import UserListSerializer

class UserlistView(APIView, CustomPageNumberPagination):

    def get(self, request):

        userlist = Userlist.objects.all()
        result_page = self.paginate_queryset(userlist, request, view=self)
        serializer = UserListSerializer(result_page, many=True)
        serializer_data = []

        for values in serializer.data:
            serializer_data.append(values)

        return self.get_paginated_response(serializer_data)

""" class UserlistView(APIView):

    def get(self, _: Request):

        userlist = Userlist.objects.all()
        serialized = UserListSerializer(instance=userlist, many=True)

        return Response({
            "My animes list": serialized.data
        }, status.HTTP_200_OK)
 """

class UserlistViewDetail(APIView):
    pass

    """ def post(self, request, anime_id):

        serializer = UserListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user.id, anime=anime_id)
        serializer_data = serializer_data
        return Response(serializer_data, status.HTTP_201_CREATED)

    def patch(self, request, anime_id):

        try: 

            anime = get_object_or_404(Anime, pk=anime_id)

            serialized = AnimeSerializer(instance=anime, data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except KeyError as key:

            return Response(
                {"message": f"You can not update {key} property"},
                status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        except Http404:
            return Response({"error": "Anime not found"})
 """