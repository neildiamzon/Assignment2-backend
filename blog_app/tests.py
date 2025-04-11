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

