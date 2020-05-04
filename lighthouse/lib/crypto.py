import bcrypt
import binascii

from Crypto import Random


def hash_str(plaintext, salt=None):
    if not salt:
        # Default salt on runtime instead of compile time to avoid having the
        # same default salt when calling the method multiple times.
        salt = bcrypt.gensalt()
    return (bcrypt.hashpw(plaintext.encode('utf-8'), salt).decode('utf-8'),
            salt.decode('utf-8'))


def get_random_token(number_of_bytes):
    return binascii.b2a_hex(
        Random.get_random_bytes(number_of_bytes)
    ).decode('utf-8')
