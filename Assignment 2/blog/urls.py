from django.urls import path
from blog.views import views

urlpatterns = [
    path('', views.post_list, name='blog-post-list'),
    path('new/', views.post_new, name='blog-post-new'),
    path('<int:post_id>/', views.post_one, name='blog-post-one'),
    path('<int:post_id>/edit/', views.post_edit, name='blog-post-edit'),
    path('<int:post_id>/delete/', views.post_delete, name='blog-post-delete'),
]