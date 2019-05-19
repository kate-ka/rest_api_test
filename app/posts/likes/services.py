from django.contrib.auth import get_user_model
from django.core.cache import cache

from posts.models import LikePost, POST_LIKE_COUNT_CACHE_KEY


User = get_user_model()


def add_like(post, user):
    like, is_created = LikePost.objects.get_or_create(user=user, post=post)
    cache.delete(POST_LIKE_COUNT_CACHE_KEY.format(post_id=post.id))
    return like


def remove_like(post, user):
    LikePost.objects.filter(post=post, user=user).delete()
    cache.delete(POST_LIKE_COUNT_CACHE_KEY.format(post_id=post.id))


def is_liked_by_user(post, user) -> bool:
    likes = LikePost.objects.filter(post=post, user=user)
    return likes.exists()


def get_all_users_who_liked_post(post):
    return User.objects.filter(user_likes__post=post).distinct().values_list('email', flat=True)