import configparser
import contextlib
from unittest import TestCase
from unittest.mock import MagicMock

from aiohttp.test_utils import AioHTTPTestCase

from lighthouse.app import init_app
from lighthouse.db import init_sqlalchemy, commit, Base, session_factory
from lighthouse.lib.crypto import hash_str
from lighthouse.lib.settings import update_settings

MagicMock.__await__ = lambda x: async_mock().__await__()


class DBMixin:
    @classmethod
    def read_settings(cls):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        config.read('test.ini')
        update_settings(config)

    def setup_sqlalchemy(self):
        init_sqlalchemy()
        self.session = session_factory()

    def persist_all(self, data):
        self.session.add_all(data)
        commit()

    def emptyTables(self):
        with contextlib.closing(Base.metadata.bind.connect()) as con:
            trans = con.begin()
            for table in reversed(Base.metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()
        self.session.close()


class TestCaseWithDB(TestCase, DBMixin):
    @classmethod
    def setUpClass(cls):
        cls.read_settings()

    def setUp(self):
        self.setup_sqlalchemy()

    def tearDown(self):
        self.emptyTables()


class AioHTTPTestCaseWithDB(AioHTTPTestCase, DBMixin):
    username = "test"
    password = "test1234!?"

    @classmethod
    def setUpClass(cls):
        cls.read_settings()

    def setUp(self):
        super().setUp()
        self.setup_sqlalchemy()

    def tearDown(self):
        super().tearDown()
        self.emptyTables()

    async def get_application(self):
        hashed_password, salt = hash_str(self.password)
        auth_settings = {
            'user': {
                'username': self.username,
                'hashed_password': hashed_password,
                'salt': salt
            }
        }
        update_settings(auth_settings)
        return init_app()

    async def login(self):
        await self.client.post("/auth/login", json={
            'username': self.username,
            'password': self.password
        })


async def async_mock():
    pass
