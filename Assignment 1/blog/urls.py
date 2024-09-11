from django.urls import path
from blog.views import views

urlpatterns = [
    path('hello', views.hello_view),
    path('posts/', views.post_list),
    path('posts/<int:post_id>/', views.post_one, name='blog-views-post'),
]