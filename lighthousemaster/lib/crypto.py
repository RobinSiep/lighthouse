import binascii

from Crypto import Random


def get_random_token(number_of_bytes):
    return binascii.b2a_hex(
        Random.get_random_bytes(number_of_bytes)
    ).decode('utf-8')
