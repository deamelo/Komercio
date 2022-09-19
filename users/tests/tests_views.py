from rest_framework.test import APITestCase
from rest_framework.views import status

from django.urls import reverse

from users.models import User


class UserRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse('user')

        cls.seller = {
            "username": "Vendedor",
            "password": "abcd",
            "first_name": "Vendedor",
            "last_name": "dos Santos",
            "is_seller": True
        }

        cls.seller_fail = {
            "username": "Vendedor",
            "first_name": "Vendedor",
            "last_name": "dos Santos",
            "is_seller": True
        }

        cls.buyer = {
            "username": "Comprador",
            "password": "abcd",
            "first_name": "Comprador",
            "last_name": "de Sousa",
            "is_seller": False
        }

        cls.buyer_fail = {
            "username": "Comprador",
            "password": "abcd",
            "last_name": "de Sousa",
            "is_seller": False
        }

    def test_register_seller(self):
        response = self.client.post(self.base_url, data=self.seller)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_register_buyer(self):
        response = self.client.post(self.base_url, data=self.buyer)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_register_seller_fields_fail(self):
        response = self.client.post(self.base_url, data=self.seller_fail)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_register_buyer_fields_fail(self):
        response = self.client.post(self.base_url, data=self.buyer_fail)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)


class LoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("login")

        cls.seller_credentials = {"username": "Vendedor", "password": "abcd"}
        cls.seller_data = {
            "username": "Vendedor",
            "password": "abcd",
            "first_name": "Vendedor",
            "last_name": "dos Santos",
            "is_seller": True
        }
        cls.seller = User.objects.create_user(**cls.seller_data)

        cls.buyer_credentials = {"username": "Comprador", "password": "abcd"}
        cls.buyer_data = {
            "username": "Comprador",
            "password": "abcd",
            "first_name": "Comprador",
            "last_name": "de Sousa",
            "is_seller": False
        }
        cls.buyer = User.objects.create_user(**cls.buyer_data)

    def test_token_field_seller_is_returned(self):
        response = self.client.post(self.base_url, data=self.seller_credentials)

        self.assertIn("token", response.data)

    def test_token_field_buyer_is_returned(self):
        response = self.client.post(self.base_url, data=self.buyer_credentials)

        self.assertIn("token", response.data)
