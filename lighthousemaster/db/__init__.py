from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

from lighthousemaster.lib.settings import settings

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


def get_connection_url(settings_):
    return "{driver}://{user}:{password}@{host}/{database}".format(
        driver=settings_['sqlalchemy.driver'],
        user=settings_['sqlalchemy.user'],
        password=settings_['sqlalchemy.password'],
        host=settings_['sqlalchemy.host'],
        database=settings_['sqlalchemy.database']
    )


def init_sqlalchemy():
    engine = create_engine(get_connection_url(settings))
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
