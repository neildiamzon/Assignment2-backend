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
