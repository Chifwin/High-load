from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from shop.models import Order, Product
from shop.serializers import OrderSerializer

class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            order = Order.objects.get(status=Order.Status.CREATED)
        except Order.DoesNotExist:
            order = Order.objects.create(user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.Status.CANCELLED
        order.items.clear()
        order.save()
        return Response(status=status.HTTP_200_OK)

class OrderProductView(APIView):
    def put(self, requst, pk, prod_id):
        order = get_object_or_404(Order, pk=pk)
        if order.status != Order.Status.CREATED:
            return Response(status=status.HTTP_403_FORBIDDEN)
        get_object_or_404(Product, pk=prod_id)
        order.items.add(prod_id)
        order.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk, prod_id):
        order = get_object_or_404(Order, pk=pk)
        if order.status != Order.Status.CREATED:
            return Response(status=status.HTTP_403_FORBIDDEN)
        order.items.remove(prod_id)
        order.save()
        return Response(status=status.HTTP_200_OK)

class OrderPayView(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status != Order.Status.CREATED:
            return Response(status=status.HTTP_403_FORBIDDEN)
        order.status = Order.Status.PAID
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
