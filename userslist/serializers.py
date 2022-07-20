from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, Userlist
from animes.models import Anime

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userlist
        fields = "__all__"

    def create(self, validated_data):

        user = get_object_or_404(User, pk=validated_data["user"])
        anime = get_object_or_404(Anime, pk=validated_data["anime"])
        
        validated_data["user"] = user 
        validated_data["anime"] = anime 
        user_list = Userlist.objects.create(**validated_data)

        return user_list