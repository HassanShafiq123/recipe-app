from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, User
from recipe.serializer import TagSerializer


TAG_URL = reverse('recipe:tag-list')


class PublicTagApiTests(TestCase):
    """Test the publicaly available tags API"""

    def setUp(self) -> APIClient:
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        response = self.client.get(TAG_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@test.com',
            'testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name="Dessert")

        response = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'otheruser@test.com',
            'testpass123'
        )
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name='Comfort food')

        resposne = self.client.get(TAG_URL)

        self.assertEqual(resposne.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposne.data), 1)
        self.assertEqual(resposne.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {"name": "Test tag"}
        self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {"name": ""}
        response = self.client.post(TAG_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)