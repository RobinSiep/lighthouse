import base64
import datetime
import uuid
from unittest import TestCase

from aiohttp.test_utils import make_mocked_request

from lighthouse.lib.crypto import get_random_token
from lighthouse.lib.security import validate_access_token
from lighthouse.models.oauth import OAuthAccessToken, OAuthClient
from lighthouse.tests import TestCaseWithDB


class TestValidateAccessToken(TestCaseWithDB):
    def setUp(self):
        super().setUp()
        self.insert_test_data()

    def insert_test_data(self):
        client_id = uuid.uuid4()
        self.active_token_str = get_random_token(32)
        self.expired_token_str = get_random_token(32)
        self.fake_token_str = get_random_token(32)

        client = OAuthClient(
            id=client_id,
            client_type='confidential',
            name="test"
        )
        active_token = OAuthAccessToken(
            client_id=client_id,
            access_token=self.active_token_str,
            expiry_date=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        expired_token = OAuthAccessToken(
            client_id=client_id,
            access_token=self.expired_token_str,
            expiry_date=datetime.datetime.now()
        )
        self.persist_all((client, active_token, expired_token))

    def test_valid_access_token(self):
        req = self.build_mock_request('Bearer', self.active_token_str)
        self.assertTrue(validate_access_token(req))

    def test_no_auth_header(self):
        self.assertFalse(validate_access_token(
            make_mocked_request('GET', '/')
        ))

    def test_wrong_auth_method(self):
        req = self.build_mock_request('Basic', self.active_token_str)
        self.assertFalse(validate_access_token(req))

    def test_no_access_token_found(self):
        req = self.build_mock_request('Bearer', self.fake_token_str)
        self.assertFalse(validate_access_token(req))

    def test_invalid_access_token(self):
        req = self.build_mock_request('Bearer', self.expired_token_str)
        self.assertFalse(validate_access_token(req))

    def build_mock_request(self, method, token):
        req = make_mocked_request('GET', '/', headers={
            'Authorization': f"{method} {token}"
        })
        return req


class TestExtractClientAuthorization(TestCase):
    def build_mock_request(self, method, client_id):
        encoded_creds = base64.b64encode(
            f"{client_id}:{self.client_secret}".encode('utf-8')
        ).decode('utf-8')
        req = make_mocked_request('GET', '/', headers={
            'Authorization': f"{method} {encoded_creds}"
        })
        return req
