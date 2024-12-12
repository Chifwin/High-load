from django.urls import path

from main.views import products, wishlist, shopping_cart, orders

urlpatterns = [
    path("categories/", products.CategoryAllView.as_view({
        "get": "list",
        "post": "create",
    })),
    path("categories/<int:pk>/", products.CategoryDetailView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),

    path("products/", products.ProductAllView.as_view({
        "get": "list",
        "post": "create",
    })),
    path("products/<int:pk>/", products.ProductDetailView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),
    path("products/<int:pk>/reviews/", products.ProductReviewAllView.as_view()),

    path("reviews/", products.ReviewAllView.as_view({
        "get": "list",
        "post": "post"
    })),
    path("reviews/<int:pk>/", products.ReviewDetailView.as_view({
        "get": "get",
        "put": "put",
        "delete": "delete"
    }))
] + [
    path("wishlist/", wishlist.WishlistViewSet.as_view({
        "get": "get",
        "post": "post",
        "delete": "delete"
    }))
] + [
    path("shopping_cart/", shopping_cart.ShoppingCartViewSet.as_view({
        "get": "get",
        "post": "post",
        "delete": "delete"
    })),
    path("shopping_cart/order/", shopping_cart.ShoppingCartViewSet.as_view({
        "post": "make_order"
    }))
] + [
    path("orders/", orders.OrderViewSet.as_view({
        "get": "get_all"
    })),
    path("orders/<int:pk>/", orders.OrderViewSet.as_view({
        "get": "get_one",
        "put": "put"
    })),
]