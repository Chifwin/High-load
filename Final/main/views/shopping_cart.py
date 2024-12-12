from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Order, OrderItem, CartItem, ShoppingCart
from main.serializers import ShoppingCartSerializer, CartItemSerializer


class ShoppingCartViewSet(viewsets.GenericViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCart.objects.all()

    def make_order(self, request):
        try:
            cart = self.queryset.get(user_id=request.user)
        except ShoppingCart.DoesNotExist:
            return Response({"detail": "Shopping cart doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        if len(cart.items.all()) == 0:
            return Response({"detail": "Order cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user_id=request.user)
        for item in cart.items.all():
            OrderItem.objects.create(
                order_id=order, product_id=item.product_id, quantity=item.quantity, price=item.product_id.price
            )
            item.delete()
        return Response(data={"order_id": order.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        cart, _ = self.queryset.get_or_create(user_id=request.user)
        serializer = ShoppingCartSerializer(cart)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = self.queryset.get_or_create(user_id=request.user)
        cart_item, created_item = CartItem.objects.get_or_create(product_id=serializer.validated_data["product_id"],
                                                                 cart_id=cart)
        cart_item.quantity += serializer.validated_data.get("quantity", 0)
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = self.queryset.get_or_create(user_id=request.user)
        try:
            cart_item = CartItem.objects.get(product_id=serializer.validated_data["product_id"], cart_id=cart)
            if cart_item.quantity > serializer.validated_data.get("quantity", 1):
                cart_item.quantity -= serializer.validated_data.get("quantity", 1)
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
