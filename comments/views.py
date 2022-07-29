from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from animes.models import Comment
from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from rates.permissions import HasToken
from django.http import Http404
from animes.models import Anime
from animes.serializers import AnimeReturnSerializer
import ipdb


class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]

    def post(self, request: Request):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )
        try:
            get_object_or_404(Anime, pk=request.data["anime_id"])
        except Http404:
            return Response({"message": "Anime not found."}, status.HTTP_404_NOT_FOUND)
        request.data["user_id"] = token.user_id
        serialized = CommentSerializer(data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)


class CommentAnimeIdView(APIView):
    def get(self, request: Request, anime_id: str):

        try:
            get_object_or_404(Anime, pk=anime_id)
        except Http404:
            return Response({"message": "Anime not found."}, status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(anime_id=anime_id)
        serialized = CommentSerializer(instance=comments, many=True)

        if len(serialized.data) == 0:
            return Response(
                {"message": "Any comment about this anime"}, status.HTTP_404_NOT_FOUND
            )

        return Response(serialized.data, status.HTTP_200_OK)


class CommentIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]

    def patch(self, request: Request, comment_id: str):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.user.id != token.user_id:
            return Response(
                {"detail": "You do not own the comment"}, status.HTTP_403_FORBIDDEN
            )

        try:

            serialized = CommentSerializer(comment, request.data, partial=True)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status.HTTP_201_CREATED)
        except KeyError as err:

            return Response(err.args[0], err.args[1])

    def delete(self, request: Request, comment_id: str):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )

        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.user.id != token.user_id:

            return Response(
                {"detail": "You do not own the comment"}, status.HTTP_403_FORBIDDEN
            )

        comment.delete()

        return Response("", status.HTTP_204_NO_CONTENT)
