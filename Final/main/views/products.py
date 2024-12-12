from django.db.utils import IntegrityError

from rest_framework import serializers, status, mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.models import Category, Product, Review
from main.serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ReviewAddSerializer


class CategoryAllView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductAllView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductReviewAllView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["pk"])


class ReviewAllView(GenericViewSet, mixins.ListModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = ReviewAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user_id"] = request.user
        try:
            serializer.save()
        except IntegrityError:
            return Response({
                "detail": "Review to this product already exists"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["pk"])

    def get(self, request, pk):
        review = self.get_object()
        serializer = self.serializer_class(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object()
        if review.user_id != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        review = self.get_object()
        if review.user_id != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(self.serializer_class(review).data, status=status.HTTP_200_OK)
