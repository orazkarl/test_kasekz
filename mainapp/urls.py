from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
]
