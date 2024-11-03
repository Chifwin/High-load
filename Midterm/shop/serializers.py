from rest_framework import serializers
from shop.models import Category, Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)
    class Meta:
        model = Order
        fields = ("id", "user", "created_at", "updated_at", "status", "items", "total_price")
