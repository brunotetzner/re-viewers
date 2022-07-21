from rest_framework import serializers, status
from animes.models import Rate
from users.serializers import UserSerializer
from animes.serializers import AnimeReturnSerializer


class RateSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    anime_id = serializers.CharField(write_only=True)
    user_id = serializers.UUIDField(write_only=True)
    anime = AnimeReturnSerializer(read_only=True)
    rate = serializers.FloatField(min_value=0, max_value=5, write_only=True)
    gived_rate = serializers.FloatField(read_only=True, source="rate")
    

    def create(self, validated_data):
        return Rate.objects.create(**validated_data)

    def update(self, instance: Rate, validated_data: dict):
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
