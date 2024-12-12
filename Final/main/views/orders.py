from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Order, OrderItem, Payment
from main.serializers import OrderSerializer

class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user)

    def get_all(self, request):
        orders = self.get_queryset()
        return Response(self.serializer_class(orders, many=True).data, status=status.HTTP_200_OK)

    def get_one(self, request, pk):
        order = self.get_object()
        return Response(self.serializer_class(order).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        if "status" not in request.data:
            return Response({"status": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        order = self.get_object()
        order.order_status = request.data["status"]
        order.save()
        return Response(self.serializer_class(order).data, status=status.HTTP_200_OK)
