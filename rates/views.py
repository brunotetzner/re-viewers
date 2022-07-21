from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from animes.models import Rate, Anime
from animes.serializers import AnimeSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from .serializers import RateSerializer
from .permissions import HasToken


class RatesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]
    
    def post(self, request: Request):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )

        try:
            queryset = Rate.objects.filter(user_id=token.user_id, anime_id= request.data["anime_id"])
            queryset[0]
            return Response(
                {"error": "You already gave a note to this anime!"}, status.HTTP_400_BAD_REQUEST
            )
        except:
            request.data["user_id"] = token.user_id
            serialized = RateSerializer(data=request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            rates = Rate.objects.filter(anime_id=request.data["anime_id"])
            average = 0

            for rate in rates:
                average = rate.rate + average

            anime = get_object_or_404(Anime, pk=request.data["anime_id"])

            serialized_anime = AnimeSerializer(
                anime, {"average_rate": average / len(rates)}, partial=True
            )
            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            return Response(serialized.data, status.HTTP_201_CREATED)
        
        
class RatesIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]


    def patch(self, request: Request, anime_id: str):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )

        try:
            rate = get_object_or_404(Rate, user_id=token.user_id, anime_id=anime_id)

            serialized = RateSerializer(rate, request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()

            rates = Rate.objects.filter(anime_id=rate.anime.id)
            average = 0

            for rate in rates:
                average = rate.rate + average

            anime = get_object_or_404(Anime, pk=anime_id)

            serialized_anime = AnimeSerializer(
                anime, {"average_rate": average / len(rates)}, partial=True
            )
            serialized_anime.is_valid(raise_exception=True)
            serialized_anime.save()

            updated_rate = get_object_or_404(Rate, user_id=token.user_id)
            serialized = RateSerializer(updated_rate)

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"message": "Rate not found."}, status.HTTP_404_NOT_FOUND)