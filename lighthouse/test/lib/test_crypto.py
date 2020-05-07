from unittest import TestCase

from lighthouse.lib.crypto import get_random_token, hash_str


class TestHashStr(TestCase):
    def test_given_salt(self):
        expected_hash = '$2b$12$za0avPx11NmhJbk6so4xfOJgCXAp9dJj9SBF7YOl9jKI40M.3KTye'  # noqa
        salt = '$2b$12$za0avPx11NmhJbk6so4xfO'

        result_hash, result_salt = hash_str("test data", salt.encode('utf-8'))

        self.assertEqual(result_hash, expected_hash)
        self.assertEqual(result_salt, salt)

    def test_invalid_given_salt(self):
        with self.assertRaisesRegex(ValueError, "Invalid salt"):
            hash_str('testing', b'invalid')

    def test_generated_salt(self):
        result_hash_1, result_salt_1 = hash_str("test data")
        result_hash_2, result_salt_2 = hash_str("test data")
        confirmation_hash, _ = hash_str("test data",
                                        result_salt_1.encode('utf-8'))

        self.assertNotEqual(result_salt_1, result_salt_2)
        self.assertEqual(result_hash_1, confirmation_hash)


class TestGetRandomToken(TestCase):
    def test_random(self):
        self.assertNotEqual(get_random_token(32), get_random_token(32))

    def test_negative_number(self):
        with self.assertRaisesRegex(
                ValueError, "Number of bytes can't be negative"):
            get_random_token(-1)
