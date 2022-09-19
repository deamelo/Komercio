from django.test import TestCase

from products.models import Product
from users.models import User


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.description = "description"
        cls.price = 10.00
        cls.quantity = 10
        cls.is_active = True
        cls.seller = {"username": "username", "password": "password", "first_name": "first_name", "last_name": "last_name", "is_seller": True}

        seller = {"username": "username", "password": "password", "first_name": "first_name", "last_name": "last_name", "is_seller": True}

        cls.user_test = User.objects.create_user(**seller)

        cls.product_test = Product.objects.create(
            description= cls.description,
            price= cls.price,
            quantity = cls.quantity,
            is_active = cls.is_active,
            seller = cls.user_test,
        )

        cls.product_test_default_is_active = Product.objects.create(
            description= cls.description,
            price= cls.price,
            quantity = cls.quantity,
            seller = cls.user_test,
        )

    def test_product_fields_and_relationships(self):
        self.assertEqual(self.product_test.description, self.description)
        self.assertEqual(self.product_test.price, self.price)
        self.assertEqual(self.product_test.quantity, self.quantity)
        self.assertEqual(self.product_test.is_active, self.is_active)
        self.assertEqual(self.product_test.seller, self.user_test)


    def test_decimal_places_price(self):
        expected = 2
        result = self.product_test._meta.get_field("price").decimal_places

        self.assertEqual(result, expected)

    def test_max_digits_price(self):
        expected = 10
        result = self.product_test._meta.get_field("price").max_digits

        self.assertEqual(result, expected)

    # def test_positive_validator_quantity(self):
    #     expected = 0
    #     result = self.product_test._meta.get_field("quantity").min_value

    #     self.assertEqual(result, expected)

    def test_is_active_default(self):
        expected = True
        result = self.product_test_default_is_active._meta.get_field("is_active").default

        self.assertEqual(result, expected)
