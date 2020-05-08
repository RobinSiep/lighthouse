import base64
import datetime
import uuid
from unittest import TestCase

from aiohttp.test_utils import make_mocked_request

from lighthouse.lib.crypto import get_random_token
from lighthouse.lib.exceptions.oauth import (
    AuthorizationHeaderNotFound, InvalidAuthorizationMethod,
    InvalidAuthorizationHeader)
from lighthouse.lib.security import (
    extract_client_authorization, validate_access_token,
    DefaultAuthorizationPolicy, LighthouseIdentityPolicy)
from lighthouse.models.oauth import OAuthAccessToken, OAuthClient
from lighthouse.test import TestCaseWithDB, async_test


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
    def setUp(self):
        self.client_id = str(uuid.uuid4())
        self.client_secret = get_random_token(32)

    def test_valid_header(self):
        req = self.build_mock_request(
            'Basic', f"{self.client_id}:{self.client_secret}")
        result = extract_client_authorization(req)

        self.assertEqual(result['client_id'], self.client_id)
        self.assertEqual(result['client_secret'], self.client_secret)

    def test_no_header(self):
        req = make_mocked_request('GET', '/')
        with self.assertRaises(AuthorizationHeaderNotFound):
            extract_client_authorization(req)

    def test_wrong_auth_method(self):
        req = self.build_mock_request(
            'Bearer', f"{self.client_id}:{self.client_secret}"
        )
        with self.assertRaises(InvalidAuthorizationMethod):
            extract_client_authorization(req)

    def test_malformed_header(self):
        req = self.build_mock_request('Basic', "test value")

        with self.assertRaises(InvalidAuthorizationHeader):
            extract_client_authorization(req)

    def build_mock_request(self, method, creds):
        encoded_creds = base64.b64encode(
            creds.encode('utf-8')
        ).decode('utf-8')
        req = make_mocked_request('GET', '/', headers={
            'Authorization': f"{method} {encoded_creds}"
        })
        return req


class TestAuthorizedUserid(TestCase):
    def setUp(self):
        self.policy = DefaultAuthorizationPolicy('test')

    @async_test
    async def test_correct_identity(self):
        self.assertEqual(await self.policy.authorized_userid('test'), 'test')
        self.assertEqual(await self.policy.authorized_userid('oauth'), 'oauth')

    @async_test
    async def test_incorrect_identity(self):
        self.assertEqual(await self.policy.authorized_userid('nonexistent'),
                         None)


class TestPermits(TestCase):
    def setUp(self):
        self.policy = DefaultAuthorizationPolicy('test')

    @async_test
    async def test_user_permits(self):
        identity = 'test'
        self.assertTrue(await self.policy.permits(identity, 'connect'))
        self.assertTrue(await self.policy.permits(identity, 'wake_on_lan'))
        self.assertFalse(await self.policy.permits(identity, 'identify'))

    @async_test
    async def test_oauth_permits(self):
        identity = 'oauth'
        self.assertTrue(await self.policy.permits(identity, 'connect'))
        self.assertTrue(await self.policy.permits(identity, 'identify'))
        self.assertFalse(await self.policy.permits(identity, 'wake_on_lan'))

    @async_test
    async def test_no_permits(self):
        identity = 'fake'
        self.assertTrue(await self.policy.permits(identity, 'connect'))
        self.assertFalse(await self.policy.permits(identity, 'identify'))
        self.assertFalse(await self.policy.permits(identity, 'wake_on_lan'))


class TestIdentify(TestCaseWithDB):
    def setUp(self):
        super().setUp()
        self.insert_test_data()
        self.policy = LighthouseIdentityPolicy()

    def insert_test_data(self):
        client_id = uuid.uuid4()
        self.token = get_random_token(32)

        client = OAuthClient(
            id=client_id,
            client_type='confidential',
            name="test"
        )
        active_token = OAuthAccessToken(
            client_id=client_id,
            access_token=self.token,
            expiry_date=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        self.persist_all((client, active_token))

    @async_test
    async def test_identify_oauth(self):
        req = make_mocked_request('GET', '/', headers={
            'Authorization': f"Bearer {self.token}"
        })
        self.assertEqual(await self.policy.identify(req), 'oauth')
