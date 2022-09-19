from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from products.models import Product
from users.models import User


class ProductTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/products/"

        cls.seller = {
            "username": "Vendedor",
            "password": "abcd",
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

        cls.product = {
            "description": "testando",
            "price": 210.99,
            "quantity": 5
        }

        cls.product_fail = {
            "description": "testando",
            "quantity": 5
        }

        seller_user = User.objects.create_user(**cls.seller)
        cls.seller_token = Token.objects.create(user=seller_user)

        buyer_user = User.objects.create_user(**cls.buyer)
        cls.buyer_token = Token.objects.create(user=buyer_user)

        cls.product_test = Product.objects.create(**cls.product, seller=seller_user)

        cls.base_detail_url = f"/api/products/{cls.product_test.id}/"

    def test_create_product_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)

        response = self.client.post(
            self.base_url, data=self.product, format='json'
        )

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_create_product_buyer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.buyer_token.key)

        response = self.client.post(
            self.base_url, data=self.product, format='json'
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_create_product_fields_fail(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)

        response = self.client.post(
            self.base_url, data=self.product_fail, format='json'
        )

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_verify_return_fields_post(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)

        response = self.client.post(self.base_url, data=self.product)

        expected_return_fields = ("id", "description", "price", "quantity", "is_active", "seller")

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_list_products(self):
        response = self.client.get(self.base_url, data=self.product)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_list_one_product(self):
        response = self.client.get(self.base_detail_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_update_product_owner_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response = self.client.patch(
            self.base_detail_url, data={"description": "passou"}, format='json'
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)

    def test_update_product_buyer(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.buyer_token.key)
        response = self.client.patch(
            self.base_detail_url, data={"description": "não passou"}, format='json'
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)
