from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from posts.likes import services as like_services
from posts.models import Post
from posts.serializers import PostSerializer


class RetrievePostView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer


class ListCreatePostView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikePostView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, id=kwargs.get('post_id'))
        like_services.add_like(user=request.user, post=post)
        return Response(status=HTTP_204_NO_CONTENT)


class UnlikePostView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, id=kwargs.get('post_id'))
        like_services.remove_like(user=request.user, post=post)
        return Response(status=HTTP_204_NO_CONTENT)

