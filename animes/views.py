from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from .models import Anime
from rest_framework.permissions import IsAuthenticated
from .serializers import AnimeSerializer, AnimeWithCategorySerializer
from .permissions import HasPermission
from rest_framework.views import APIView, Request, Response, status
from categories.serializers import CategorySerializer
from categories.models import Category
from rest_framework import generics


class AnimeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]

    def get(self, request):

        animes = Anime.objects.all()
        serialized = AnimeWithCategorySerializer(instance=animes, many=True)

        return Response(serialized.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serialize_anime = AnimeWithCategorySerializer(data=request.data)
        serialize_anime.is_valid(raise_exception=True)

        serialize_anime = AnimeSerializer(data=request.data)
        serialize_anime.is_valid(raise_exception=True)

        try:
            create_anime = Anime.objects.create(**serialize_anime.validated_data)
            categories = request.data["categories"]
            for category in categories:

                serialize_category = CategorySerializer(data=category)
                serialize_category.is_valid(raise_exception=True)
                create_category = Category.objects.get_or_create(
                    **serialize_category.validated_data
                )

            create_anime.categories.add(create_category[0])
            serialize_anime = AnimeWithCategorySerializer(instance=create_anime)

            return Response(serialize_anime.data, status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"detail": "The anime already exists"}, status.HTTP_409_CONFLICT
            )


class AnimeIdView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]

    queryset = Anime.objects.all()
    serializer_class = AnimeWithCategorySerializer

    lookup_field = "id"

    def patch(self, request: Request, id: str):
        if not request.data:
            return Response(
                {"detail": "Need to inform some key."},
                status.HTTP_403_FORBIDDEN,
            )
        try:
            serialized_anime = AnimeWithCategorySerializer(
                data=request.data, partial=True
            )
            serialized_anime.is_valid(raise_exception=True)

            anime = get_object_or_404(Anime, pk=id)

            serialized_anime = AnimeWithCategorySerializer(
                instance=anime, data=request.data, partial=True
            )
            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            return Response(serialized_anime.data, status.HTTP_200_OK)

        except IntegrityError:
            return Response(
                {"detail": "The anime already exists"}, status.HTTP_409_CONFLICT
            )


class AnimeByCategory(APIView):
    def get(self, request: Request):
        data = []
        data_id = []
        category_not_exists = []
        animes_category_not_exists = []

        for k in request.query_params.keys():
            category_id = Category.objects.filter(category__icontains=k).first()

            if not category_id:
                category_not_exists.append(k)
                continue

            animes_in_category = Anime.objects.filter(categories=category_id.id).all()

            if not animes_in_category:
                animes_category_not_exists.append(k)
                continue

            serialized = AnimeWithCategorySerializer(animes_in_category, many=True)

            if serialized.data[0]["id"] not in data_id:
                data_id.append(serialized.data[0]["id"])
                data.append(serialized.data)

        if category_not_exists:
            return Response(
                {"data": data, "category_not_exists": category_not_exists},
                status.HTTP_200_OK,
            )

        if animes_category_not_exists:
            return Response(
                {
                    "data": data,
                    "animes_category_not_exists": animes_category_not_exists,
                },
                status.HTTP_200_OK,
            )
        return Response(data, status.HTTP_200_OK)


class RetrieveAnimeView(generics.RetrieveAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeWithCategorySerializer


class GetByRateView(generics.ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = AnimeWithCategorySerializer

    def get_queryset(self):
        max_animes = self.kwargs["anime_amount"]
        return self.queryset.order_by("-average_rate")[0:max_animes]
    