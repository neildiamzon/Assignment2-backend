from urllib import request

from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import BlogPost
from .serializers import BlogPostSerializer

from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=200)

class UserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Authenticated user: {self.request.user}")
        serializer.save(author=self.request.user)  # Save the author (current logged-in user)

class BlogPostUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)  # Allow updates only to the author's posts


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.all()  # View all blog posts (including those by other users)

class BlogPostMyView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)  # View only the logged-in user's blog posts

class BlogPostDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)