from functools import partial
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from animes.models import Anime, Comment
from animes.serializers import AnimeSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from rates.permissions import HasToken


class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasToken]

    def post(self, request: Request):
        token = Token.objects.get(
            key=self.request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        )
        get_object_or_404(Comment, pk=request.data["anime_id"])
        request.data["user_id"] = token.user_id
        serialized = CommentSerializer(data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)


class CommentAnimeIdView(APIView):
    def get(self, request: Request, anime_id: str):
        comments = Comment.objects.filter(anime_id=anime_id)
        serialized = CommentSerializer(instance=comments, many=True)
        return Response(serialized.data, status.HTTP_201_CREATED)


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
