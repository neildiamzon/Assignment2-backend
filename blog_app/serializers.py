from django.contrib.auth.models import User
from rest_framework import serializers

from blog_app.models import BlogPost


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Make the image field optional for updates

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'image']
        read_only_fields = ['id', 'author']  # author cannot be set from the request

