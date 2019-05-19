from django.urls import path

from posts import views

urlpatterns = [
    path('', views.ListCreatePostView.as_view(), name='posts_list_create'),
    path('<int:pk>', views.RetrievePostView.as_view(), name='post_detail'),
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('unlike/<int:post_id>/', views.UnlikePostView.as_view(), name='unlike_post'),
]
