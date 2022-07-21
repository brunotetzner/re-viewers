from rest_framework import serializers, status
from .models import Anime
from categories.serializers import CategorySerializer


class AnimeSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    image = serializers.CharField()
    title = serializers.CharField(max_length=128)
    sinopse = serializers.CharField(max_length=512)
    studio = serializers.CharField(max_length=30)
    banner = serializers.CharField(max_length=128)
    status = serializers.CharField()
    original_title = serializers.CharField(max_length=50)
    launch_data = serializers.DateField()
    average_rate = serializers.FloatField()

    def update(self, instance: Anime, validated_data: dict):
        non_updatable = {
            "id",
            "image",
            "title",
            "sinopse",
            "studio",
            "banner",
            "status",
            "original_title",
            "launch_data",
        }

        for key, value in validated_data.items():
            if key in non_updatable:
                raise KeyError(
                    {"message": f"You can not update the {key} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            setattr(instance, key, value)
            instance.save()

        return instance


class AnimeWithCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    image = serializers.CharField()
    title = serializers.CharField(max_length=128)
    sinopse = serializers.CharField(max_length=512)
    studio = serializers.CharField(max_length=30)
    banner = serializers.CharField(max_length=128)
    status = serializers.CharField()
    original_title = serializers.CharField(max_length=50)
    launch_data = serializers.DateField()
    average_rate = serializers.FloatField()
    categories = CategorySerializer(many=True)


class AnimeReturnSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    average_rate = serializers.FloatField()
