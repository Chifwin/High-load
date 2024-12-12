from rest_framework import serializers

from .models import Category, Product, Review, Wishlist, WishlistItem, ShoppingCart, CartItem, Order, OrderItem, Payment


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


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ["cart_id"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
