from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Order, OrderItem
from main.models import CartItem, ShoppingCart


class ShoppingCartViewSet(viewsets.GenericViewSet):
    class ShoppingCartSerializer(serializers.ModelSerializer):
        class CartItemSerializer(serializers.ModelSerializer):
            class Meta:
                model = CartItem
                fields = "__all__"

        items = CartItemSerializer(many=True)

        class Meta:
            model = ShoppingCart
            fields = "__all__"

    class ShoppingCartRequestSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField(default=1)

    class ShoppingCartMakeOrderSerializer(serializers.Serializer):
        items = serializers.ListField(
            child=serializers.IntegerField(), required=False, default=list
        )

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.all()

    def make_order(self, request):
        serializer = self.MakeOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.queryset.get(user=request.user)
        if not serializer.validated_data["items"]:
            cart_items = cart.items.all()
        else:
            cart_items = cart.items.filter(id__in=serializer.validated_data["items"])

        if not cart_items.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order, product=cart_item.product, quantity=cart_item.quantity
            )
            cart_item.delete()
        order.save()
        return Response(data={"order_id": order.id}, status=status.HTTP_201_CREATED)

    def get_shopping_cart(self, request):
        cart, _ = self.queryset.get_or_create(user=request.user)
        serializer = self.ShoppingCartSerializer(cart)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def add_product(self, request):
        serializer = self.RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = self.queryset.get_or_create(user=request.user)
        cart_item, created_item = CartItem.objects.get_or_create(
            product_id=serializer.validated_data["product_id"], cart=cart
        )
        if created_item:
            cart_item.quantity = serializer.validated_data["quantity"]
        else:
            cart_item.quantity += serializer.validated_data["quantity"]
        cart_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete_product(self, request):
        serializer = self.RequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        cart, _ = self.queryset.get_or_create(user=request.user)
        try:
            cart_item = CartItem.objects.get(
                product_id=serializer.validated_data["product_id"], cart=cart
            )
            if cart_item.quantity > serializer.validated_data["quantity"]:
                cart_item.quantity -= serializer.validated_data["quantity"]
                cart_item.save()
            else:
                cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def clear_shopping_cart(self, request):
        cart = self.queryset.get(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
