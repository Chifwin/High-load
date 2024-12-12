from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Wishlist, WishlistItem
from main.serializers import WishlistSerializer, WishlistItemSerializer


class WishlistViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wishlist.objects.all()

    def get(self, request):
        wishlist, _ = self.queryset.get_or_create(user_id=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WishlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist, _ = self.queryset.get_or_create(user_id=request.user)
        _, created_item = WishlistItem.objects.get_or_create(
            product_id=serializer.validated_data["product_id"], wishlist_id=wishlist
        )
        return Response(status=status.HTTP_201_CREATED if created_item else status.HTTP_200_OK)

    def delete(self, request):
        serializer = WishlistItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist, _ = self.queryset.get_or_create(user_id=request.user)
        try:
            wishlist_item = WishlistItem.objects.get(
                product_id=serializer.validated_data["product_id"], wishlist_id=wishlist
            )
            wishlist_item.delete()
        except WishlistItem.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
