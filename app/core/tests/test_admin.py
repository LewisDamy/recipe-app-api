"""
Tests for the Django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client"""
        self.client = Client()  # Django test class that allows user to make HTTP Requests
        # Creating a superuser into the DB for testing purpose
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)  # force the auth for the user
        # Creating an user into the DB for testing purpose
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')  # get the URL for the list of users in the admin section
        res = self.client.get(url)  # make the HTTP GET Request for the URL (using the setUp Client instance)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])  # url: /admin/core/user/1/change/
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)
