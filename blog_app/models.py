from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Image field to upload images

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()  # Count the number of likes related to this blog post


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog_post')  # Prevent a user from liking the same post multiple times

    def __str__(self):
        return f"{self.user.username} liked {self.blog_post.title}"

