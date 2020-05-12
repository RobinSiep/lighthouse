import asyncio
import configparser
import contextlib
from unittest import TestCase

from aiohttp.test_utils import AioHTTPTestCase

from lighthouse.app import init_app
from lighthouse.db import init_sqlalchemy, commit, Base, DBSession as session
from lighthouse.lib.crypto import hash_str
from lighthouse.lib.settings import update_settings


class TestCaseWithDB(TestCase):
    def setUp(self):
        self.read_settings()
        init_sqlalchemy()

    def read_settings(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        config.read('test.ini')
        update_settings(config)

    def persist_all(self, data):
        session.add_all(data)
        commit()

    def tearDown(self):
        self.emptyTables()

    def emptyTables(self):
        with contextlib.closing(Base.metadata.bind.connect()) as con:
            trans = con.begin()
            for table in reversed(Base.metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()


class AioHTTPTestCaseWithDB(AioHTTPTestCase, TestCaseWithDB):
    username = "test"
    password = "test1234!?"

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


def async_test(f):
    def wrapper(*args, **kwargs):
        coroutine = asyncio.coroutine(f)
        future = coroutine(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper
