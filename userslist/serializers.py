from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User, Userlist
from animes.models import Anime

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userlist
        fields = "__all__"
        read_only_fields = ["user", "anime"]