from rest_framework import serializers, status

from categories.models import Category
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
    status = serializers.ChoiceField(
        allow_null=True,
        choices=(
            ("On going"),
            ("Canceled"),
            ("Finished"),
        ),
    )
    original_title = serializers.CharField(max_length=50)
    launch_data = serializers.DateField()
    categories = CategorySerializer(many=True)

    def update(self, instance: Anime, validated_data: dict):
        non_updatable = {
            "id",
        }

        for key, value in validated_data.items():
            if key in non_updatable:
                raise KeyError(
                    {"message": f"You can not update the {key} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

                # get de animes por categoria

            if key == "categories":
                lista = []
                for category in value:
                    category2, _ = Category.objects.get_or_create(
                        category=category["category"]
                    )
                    lista.append(category2)

                instance.categories.set(lista)
                continue

            setattr(instance, key, value)
            instance.save()

        return instance


class AnimeReturnSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    average_rate = serializers.FloatField()
