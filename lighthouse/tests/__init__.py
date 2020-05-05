import configparser
import contextlib
from unittest import TestCase

from lighthouse.db import init_sqlalchemy, commit, Base, DBSession as session
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
