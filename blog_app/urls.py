from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, LogoutView, BlogPostCreateView, BlogPostUpdateView, BlogPostListView, \
    BlogPostMyView, BlogPostDeleteView, LikeBlogPostView, UnlikeBlogPostView, EditUserView

router = DefaultRouter()

urlpatterns = [path('api/', include(router.urls)), path('register/', RegisterView.as_view(), name='register'),
               path('login/', LoginView.as_view(), name='login'), path('logout/', LogoutView.as_view(), name='logout'),
               path('blogposts/create/', BlogPostCreateView.as_view(), name='blogpost-create'),
               path('blogposts/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost-update'),
               path('blogposts/', BlogPostListView.as_view(), name='blogpost-list'),
               path('blogposts/my/', BlogPostMyView.as_view(), name='blogpost-my-list'),
               path('blogposts/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost-delete'),

               path('blogposts/<int:pk>/like/', LikeBlogPostView.as_view(), name='blogposts-like'),
               path('blogposts/<int:pk>/unlike/', UnlikeBlogPostView.as_view(), name='blogposts-unlike'),
               path('user/edit/', EditUserView.as_view(), name='edit-user')
               ]
