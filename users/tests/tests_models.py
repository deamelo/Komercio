from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = "username"
        cls.password = "password"
        cls.first_name = "first_name"
        cls.last_name = "last_name"
        cls.is_seller = True

        cls.user_test = User.objects.create_user(
            username= cls.username,
            password= cls.password,
            first_name = cls.first_name,
            last_name = cls.last_name,
            is_seller = cls.is_seller,
        )

        cls.user_test_default_is_seller = User.objects.create_user(
            username= "username_test",
            password= cls.password,
            first_name = cls.first_name,
            last_name = cls.last_name,
        )

    def test_user_fields(self):
        self.assertEqual(self.user_test.username, self.username)
        self.assertTrue(self.user_test.check_password(self.password))
        self.assertEqual(self.user_test.first_name, self.first_name)
        self.assertEqual(self.user_test.last_name, self.last_name)
        self.assertEqual(self.user_test.is_seller, self.is_seller)

    def test_unique_username(self):
        expected = True
        result = self.user_test._meta.get_field("username").unique

        self.assertEqual(result, expected)

    def test_max_length_first_first_name(self):
        expected = 50
        result = self.user_test._meta.get_field("first_name").max_length

        self.assertEqual(result, expected)

    def test_max_length_first_last_name(self):
        expected = 50
        result = self.user_test._meta.get_field("last_name").max_length

        self.assertEqual(result, expected)

    def test_is_seller_default(self):
        expected = False
        result = self.user_test_default_is_seller._meta.get_field("is_seller").default

        self.assertEqual(result, expected)
