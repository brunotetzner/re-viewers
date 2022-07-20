from rest_framework import serializers

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
    launch_data=serializers.DateField()


class AnimeWithCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    image = serializers.CharField()
    title = serializers.CharField(max_length=128)
    sinopse = serializers.CharField(max_length=512)
    studio = serializers.CharField(max_length=30)
    banner = serializers.CharField(max_length=128)
    status = serializers.CharField()
    original_title = serializers.CharField(max_length=50)
    launch_data=serializers.DateField()
    categories=CategorySerializer(many=True)
