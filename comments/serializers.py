from rest_framework import serializers, status
from animes.models import Comment
from users.serializers import UserCommentSerializer
from animes.serializers import AnimeReturnSerializer


class CommentSerializer(serializers.Serializer):
    comment_id = serializers.CharField(source="id",read_only=True)
    comment = serializers.CharField()
    anime_id = serializers.CharField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)
    user = UserCommentSerializer(read_only=True)
    anime = AnimeReturnSerializer(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance: Comment, validated_data: dict):
        non_updatable = {"anime_id", "user_id", "id"}

        for key, value in validated_data.items():
            if key in non_updatable:
                raise KeyError(
                    {"message": f"You can not update the {key} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            setattr(instance, key, value)
            instance.save()

        return instance
