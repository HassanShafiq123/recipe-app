from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="user@test.com", password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class TestModels(TestCase):

    def test_user_create_with_email_successfully(self):
        """Test that user is created successfully with email"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "testpass123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testpass123")

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """

        user = get_user_model().objects.create_superuser(
            "testadmin@example.com",
            "testpass@123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string represention"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)
