from rest_framework import serializers

from posts.models import Post
from posts.likes import services as likes_services


class PostSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField()
    who_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'name', 'content', 'user', 'like_count', 'is_liked_by_user', 'who_liked')
        read_only_fields = ('user', 'like_count', 'is_liked', 'who_liked')

    def get_is_liked_by_user(self, post) -> bool:
        user = self.context.get('request').user
        return likes_services.is_liked_by_user(post, user)

    def get_who_liked(self, post) -> list:
        return likes_services.get_all_users_who_liked_post(post)

    def get_like_count(self, post):
        return post.like_count

    def get_user(self, post):
        return {'id': post.user.id, 'email': post.user.email}



