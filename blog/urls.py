from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('posts/', views.post_list_view, name='post_list'),
    path('posts/create/', views.post_create_view, name='post_create'),
    path('posts/my-posts/', views.my_posts_view, name='my_posts'),
    path('posts/<slug:slug>/recommend/', views.post_recommend_view, name='post_recommend'),
    path('posts/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('posts/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('posts/<slug:slug>/', views.post_detail_view, name='post_detail'),
]


