from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from animes.models import Rate, Anime
from animes.serializers import AnimeWithCategorySerializer, AnimeRateSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from .serializers import RateSerializer
from .permissions import HasToken
import ipdb


class RatesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]

    def post(self, request: Request, anime_id: str):

        user = request.user

        try:
            anime = get_object_or_404(Anime, pk=anime_id)

            queryset = Rate.objects.filter(user_id=user.id, anime_id=anime_id)

            if queryset:
                return Response(
                    {"detail": "You already gave a note to this anime!"},
                    status.HTTP_400_BAD_REQUEST,
                )

            request.data["user_id"] = user.id
            request.data["anime_id"] = anime_id

            serialized = RateSerializer(data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            rates = Rate.objects.filter(anime_id=anime_id)
            average = 0

            for rate in rates:
                average = rate.rate + average

            serialized_anime = AnimeWithCategorySerializer(
                anime, {"average_rate": average / len(rates)}, partial=True
            )
            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            return Response(serialized.data, status.HTTP_201_CREATED)

        except Http404:
            return Response({"detail": "Anime not found."}, status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, anime_id: str):

        user = request.user

        try:
            rate = get_object_or_404(Rate, user_id=user.id, anime_id=anime_id)
            serialized = RateSerializer(rate, request.data, partial=True)

            serialized.is_valid(raise_exception=True)
            serialized.save()

            rates = Rate.objects.filter(anime_id=rate.anime.id)
            average = 0

            for rate in rates:
                average = rate.rate + average

            anime = get_object_or_404(Anime, pk=anime_id)
            new_average = {"average_rate": average / len(rates)}

            serialized_anime = AnimeRateSerializer(instance=anime, data=new_average)

            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            updated_rate = get_object_or_404(Rate, id=rate.id)
            serialized = RateSerializer(updated_rate)

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Rate not found."}, status.HTTP_404_NOT_FOUND)


class RatesIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]

    def patch(self, request: Request, anime_id: str):

        user = request.user

        try:
            rate = get_object_or_404(Rate, user_id=user.id, anime_id=anime_id)
            serialized = RateSerializer(rate, request.data, partial=True)

            serialized.is_valid(raise_exception=True)
            serialized.save()

            rates = Rate.objects.filter(anime_id=rate.anime.id)
            average = 0

            for rate in rates:
                average = rate.rate + average

            anime = get_object_or_404(Anime, pk=anime_id)
            new_average = {"average_rate": average / len(rates)}

            serialized_anime = AnimeRateSerializer(instance=anime, data=new_average)

            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            updated_rate = get_object_or_404(Rate, id=rate.id)
            serialized = RateSerializer(updated_rate)

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Rate not found."}, status.HTTP_404_NOT_FOUND)
