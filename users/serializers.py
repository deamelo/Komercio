from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "is_seller", "is_active", "is_superuser", "date_joined",]
        read_only_fields = ["is_active", "is_superuser", "date_joined",]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)

        return user


class UserFilterOrUpdateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "is_seller", "is_active", "is_superuser", "date_joined"]
        read_only_fields = ["is_active"]
        extra_kwargs = {"password": {"write_only": True}}


class UserUpdateIsActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "is_seller", "is_active", "is_superuser", "date_joined"]
        read_only_fields = ["id", "username", "first_name", "last_name", "is_seller", "is_superuser", "date_joined"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)