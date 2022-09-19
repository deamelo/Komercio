from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status, Response
from rest_framework.authtoken.models import Token

from django.urls import reverse

from users.models import User

class AuthUser(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("user")
        cls.client = APIClient

        cls.admin_data = {
            "username": "Admin",
            "password": "abcd",
            "first_name": "Admin",
            "last_name": "dos Silva",
            "is_seller": False
        }

        admin_user = User.objects.create_superuser(**cls.admin_data)
        cls.admin_token = Token.objects.create(user=admin_user)

        cls.seller_data = {
            "username": "Vendedor",
            "password": "abcd",
            "first_name": "Vendedor",
            "last_name": "dos Santos",
            "is_seller": True
        }
        seller_user = User.objects.create_user(**cls.seller_data)
        cls.seller_token = Token.objects.create(user=seller_user)

        cls.buyer_data = {
            "username": "Comprador",
            "password": "abcd",
            "first_name": "Comprador",
            "last_name": "de Sousa",
            "is_seller": False
        }

        buyer_user = User.objects.create_user(**cls.buyer_data)
        cls.buyer_token = Token.objects.create(user=buyer_user)

        cls.base_url_datail = reverse("user-datail", kwargs={"pk": seller_user.id})
        cls.base_url_admin = reverse("admin", kwargs={"pk": buyer_user.id})

    def test_owner_can_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response: Response = self.client.patch(
            self.base_url_datail, data={"last_name": "teste"}
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_cannot_update_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.buyer_token.key)
        response: Response = self.client.patch(
            self.base_url_datail, data={"last_name": "teste"}
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_cannot_update_is_active(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.buyer_token.key)
        response: Response = self.client.patch(
            self.base_url_admin, data={"is_active": False}
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_admin_can_update_is_active(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response: Response = self.client.patch(
            self.base_url_admin, data={"is_active": False}
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_user_can_list(self):
        response: Response = self.client.get(self.base_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
