from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, Userlist
from animes.models import Anime

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userlist
        fields = "__all__"
        read_only_fields = ["user", "anime"]

    """ def create(self, validated_data):

        user_id = validated_data.get("user_id")
        anime_id = validated_data.get("anime_id")

        user = get_object_or_404(User, pk=user_id)
        anime = get_object_or_404(Anime, pk=anime_id)
        
        validated_data["user"] = user 
        validated_data["anime"] = anime 
        user_list = Userlist.objects.create(**validated_data)

        return user_list """