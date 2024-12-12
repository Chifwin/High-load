from rest_framework import serializers

from .models import Category, Product, Review, Wishlist, WishlistItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user_id"]


class ReviewAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["user_id"]

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product_id"]

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True)
    class Meta:
        model = Wishlist
        fields = "__all__"
