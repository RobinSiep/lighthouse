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
        **settings['sqlalchemy']
    )


def init_sqlalchemy():
    engine = create_engine(get_connection_url(settings))
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
