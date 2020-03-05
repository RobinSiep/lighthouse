import datetime
import logging
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from lighthousemaster.db import Base, DBSession as session
from lighthousemaster.lib.crypto import get_random_token

log = logging.getLogger(__name__)


class OAuthClient(Base):
    __tablename__ = 'oauth_client'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID, default=uuid.uuid4)
    client_secret = Column(String(64), default=get_random_token(32))
    client_type = Column(Enum("confidential", name="client_type"))
    active = Column(Boolean, default=True)
    name = Column(String(100))

    def set_fields(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class OAuthAccessToken(Base):
    __tablename__ = 'oauth_access_token'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    client_id = (Column(UUID,
                        ForeignKey('oauth_client.id')))
    access_token = Column(String(64), default=get_random_token(32),
                          unique=True)
    token_type = Column(Enum("Bearer", name="token_type"), default="Bearer")
    expiry_date = Column(DateTime(timezone=True))

    client = relationship('OAuthClient')

    @property
    def expires_in(self):
        seconds_left = (self.expiry_date - datetime.datetime.now(
            datetime.timezone.utc)
        ).total_seconds()
        return seconds_left if seconds_left > 0 else 0


def get_client(client_id, client_secret):
    return session.query(OAuthClient).filter(
        OAuthClient.client_id == client_id,
        OAuthClient.client_secret == client_secret).one()
