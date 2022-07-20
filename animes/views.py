from rest_framework.generics import  ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from .models import Anime
from rest_framework.permissions import IsAuthenticated
from .serializers import AnimeSerializer
from .permissions import HasPermission
from rest_framework.views import APIView, Request, Response,  status

class ListAndCreateAnimesView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission] 
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer


# class AnimeView(APIView,
# #  PageNumberPagination
#  ):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [HasPermission]
    
#     def get(self, request):     

#         animes = Anime.objects.all()
#         pagination = self.paginate_queryset(queryset=animes, request=request, view=self)
#         serialized = AnimeSerializer(pagination, many=True)
        
#         return self.get_paginated_response(serialized.data)


        
#     def post(self, request:Request):
#         serialize_anime = AnimeSerializer(data=request.data)
#         serialize_anime.is_valid(raise_exception=True)
        
#         create_anime = Anime.objects.create(**serialize_anime.validated_data)

#         categories = request.data["categories"]
#         for genre in categories:
#             serialize_genre = categorieserializer(data=genre)
#             serialize_genre.is_valid(raise_exception=True)
#             create_genre = categories.objects.get_or_create(**serialize_genre.validated_data)
#             create_anime.categories.add(create_genre[0])

#         serialize_anime = AnimeSerializer(instance=create_anime)


#         return Response(serialize_anime.data, status.HTTP_201_CREATED)