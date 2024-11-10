# articles/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavouriteArticle


class AccessControlTests(TestCase):
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        # create a test article
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            synopsis="Test synopsis",
            content="Test content"
        )

    def test_favourites_view_requires_login(self):
        """Test that favourites view is only accessible to logged-in users"""
        response = self.client.get(reverse('favourites'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login

        # initiate login and try again
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)

    def test_publications_view_requires_login(self):
        """Test that publications view is only accessible to logged-in users"""
        response = self.client.get(reverse('publish_article'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login

        # initiate login and try again
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('publish_article'))
        self.assertEqual(response.status_code, 200)


    def test_registered_user_cannot_access_registration(self):
        """Test that a logged-in user cannot access the registration form"""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('register'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect or deny access


class FavouritesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            synopsis="Test synopsis",
            content="Test content"
        )
        self.client.login(username="testuser", password="password")

    def test_cannot_add_duplicate_favourite(self):
        """Test that a user cannot add the same article twice to their favourites"""
        # Add article to favourites
        self.client.post(reverse('add_to_favourite', args=[self.article.pk]))
        fav_count = UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count()
        self.assertEqual(fav_count, 1)

        # Try to add the same article again
        self.client.post(reverse('add_to_favourite', args=[self.article.pk]))
        fav_count = UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count()
        self.assertEqual(fav_count, 1)  # Should not increase the count
