from django.contrib.auth.models import User
from rest_framework import serializers

from blog_app.models import BlogPost, Like


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BlogPostSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)  # Include like count
    image = serializers.ImageField(required=False)  # Make the image field optional for updates

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'like_count', 'image']
        read_only_fields = ['id', 'author']  # author cannot be set from the request

# Like serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog_post', 'created_at']
        read_only_fields = ['user', 'blog_post']
