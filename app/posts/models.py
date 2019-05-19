from django.db import models
from django.conf import settings
from django.core.cache import cache


POST_LIKE_COUNT_CACHE_KEY = 'plc_{post_id}'


class Post(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    @property
    def like_count(self):
        likes_count = cache.get(POST_LIKE_COUNT_CACHE_KEY.format(post_id=self.pk))
        if not likes_count:
            likes_count = self.post_likes.all().count()
            cache.set(POST_LIKE_COUNT_CACHE_KEY.format(post_id=self.pk), likes_count)
        return likes_count


class LikePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created"]
        unique_together = ("user", "post")
