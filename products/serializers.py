from rest_framework import serializers
from .models import Product
from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    seller_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ["id", "description", "price", "quantity", "is_active", "seller_id"]


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "description", "price", "quantity", "is_active", "seller"]
        read_only_fields = ["is_active"]
