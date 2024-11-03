from django.urls import path

from shop.views import category_views, product_views, order_views

urlpatterns = [
    path("categories/", category_views.CategoriesView.as_view()),
    path("categories/<int:pk>/", category_views.CategoryView.as_view()),

    path("products/", product_views.ProductsView.as_view()),
    path("products/<int:pk>/", product_views.ProductView.as_view()),

    path("orders/", order_views.OrdersView.as_view()),
    path("orders/<int:pk>/", order_views.OrderView.as_view()),
    path("orders/<int:pk>/pay/", order_views.OrderPayView.as_view()),
    path("orders/<int:pk>/<int:prod_id>/", order_views.OrderProductView.as_view()),
]