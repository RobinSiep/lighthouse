import copy
import logging
import transaction

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

from lighthouse.lib.settings import settings

log = logging.getLogger(__name__)

session_factory = sessionmaker()
DBSession = scoped_session(session_factory)
register(DBSession)
Base = declarative_base()

from lighthouse.models.machine import *  # noqa
from lighthouse.models.network_interface import *  # noqa
from lighthouse.models.oauth import *  # noqa


def get_connection_url(settings_):
    return "{driver}://{user}:{password}@{host}/{database}".format(
        **settings['sqlalchemy']
    )


def init_sqlalchemy():
    engine = create_engine(get_connection_url(settings))
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine


def commit():
    log.debug("Committing session: %r", DBSession.dirty)
    transaction.commit()


def persist(obj):
    log.debug("persisting object %r", obj)
    DBSession.add(obj)
    DBSession.flush()
    return obj


def rollback():
    log.debug("Rolling back session: %r", DBSession.dirty)
    return DBSession.rollback()


def delete(obj):
    log.debug("deleting object %r", obj)
    DBSession.delete(obj)


def save(obj):
    try:
        obj = persist(obj)
        try:
            id_ = obj.id
        except AttributeError:
            id_ = None
        # Shallow copy to be able to return generated data without having
        # to request the object again to get it in session.
        obj_copy = copy.copy(obj)
    except Exception as e:
        log.critical(
            'Something went wrong saving the {}'.format(
                obj.__class__.__name__),
            exc_info=True)
        rollback()
        raise e
    finally:
        commit()

    return obj_copy, id_
