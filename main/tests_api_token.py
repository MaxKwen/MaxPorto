from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from main.models import Project


class TokenAuthAPITest(APITestCase):
    """Tutorial 10: login token, POST terautentikasi token, logout, dan CORS."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.token_url = reverse("api:api_token_auth")
        self.logout_url = reverse("api:api_logout")
        self.list_url = reverse("api:project-list")
        self.payload = {
            "title": "Mobile app", "description": "Flutter client", "category": "Flutter",
            "project_url": "https://example.com/", "thumbnail": "",
        }

    def obtain(self, username, password="test-password"):
        return self.client.post(
            self.token_url, {"username": username, "password": password}, format="json",
        )

    def test_obtain_token_with_valid_credentials(self):
        response = self.obtain("owner")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], Token.objects.get(user=self.owner).key)

    def test_obtain_token_rejects_wrong_password(self):
        response = self.obtain("owner", "wrong")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Token.objects.exists())

    def test_owner_token_creates_project_without_csrf(self):
        token = self.obtain("owner").data["token"]
        # Klien mobile tidak punya cookie/CSRF; header Authorization sudah cukup
        client = APIClient(enforce_csrf_checks=True)
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(title="Mobile app").exists())

    def test_visitor_token_cannot_create_project(self):
        token = self.obtain("visitor").data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token not-a-real-token")
        response = self.client.post(self.list_url, self.payload, format="json")
        # SessionAuthentication terdaftar pertama dan tidak punya header
        # WWW-Authenticate, sehingga DRF memakai 403 (bukan 401) untuk token salah
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Invalid token.")

    def test_logout_deletes_token(self):
        token = self.obtain("owner").data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(key=token).exists())
        # Token yang sudah dicabut tidak bisa dipakai lagi
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Invalid token.")

    def test_logout_requires_authentication(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cors_header_for_local_flutter_web(self):
        response = self.client.get(self.list_url, HTTP_ORIGIN="http://localhost:5000")
        self.assertEqual(response["Access-Control-Allow-Origin"], "*")
