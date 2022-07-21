from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from users.models import User
from core.exceptions import UniqueException, CurrentPasswordException


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=200, write_only=True)

    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)

    def validate_email(self, email: str):
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise UniqueException({"error": "Email already exists"})

        return email

    def create(self, validate_data):
        user = User.objects.create(**validate_data)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=200)
    current_password = serializers.CharField(max_length=200, write_only=True)

    def validate_email(self, email: str):
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise UniqueException({"error": "Email already exists"})

        return email

    def validate(self, attrs: dict):
        if attrs.get("password"):
            if not attrs.get("current_password"):
                raise CurrentPasswordException(
                    {"error": "enter current password(current_password)"}
                )

            if not check_password(
                attrs.get("current_password"), self.instance.password
            ):
                raise CurrentPasswordException({"error": "invalid current password"})
            attrs.pop("current_password")

        return attrs

    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            if key == "password":
                password = make_password(value)
                setattr(instance, key, password)
                instance.save()
                continue

            setattr(instance, key, value)
            instance.save()

        return instance
