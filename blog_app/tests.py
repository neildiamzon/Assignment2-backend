from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.db import connections
from rest_framework.authtoken.models import Token

from blog_app.models import BlogPost


class BlogAppTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @classmethod
    def tearDownClass(self):
        """Close database connections after each test"""
        connections.close_all()  # Close all database connections

    def test_create_blog_post(self):
        url = '/api/blogposts/create/'
        data = {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        print("Success blog post creation")

    def test_delete_blog_post(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )

        url = f'/api/blogposts/{blog_post.id}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)
        print("Success blog post deletion")

    def test_update_blog_post(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )

        url = f'/api/blogposts/{blog_post.id}/'
        response = self.client.put(url, 
                                   data={
                                       'title': 'Updated Blog Post',
                                       'content': 'This is an updated blog post.'
                                   },
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Success blog post UPDATE")

    def test_view_my_blog_post(self):
        url = f'/api/blogposts/my/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Success view my blog posts")

    def test_view_blog_posts(self):
        url = f'/api/blogposts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Success view all blog posts")

