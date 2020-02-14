import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from lighthousemaster.db import Base, DBSession as session


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sid = Column(String(32), unique=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)

    def set_fields(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def list_machines():
    return session.query(Machine).all()


def get_machine_by_sid(sid):
    return session.query(Machine).filter(Machine.sid == sid).one()


def get_machine_by_name(name):
    return session.query(Machine).filter(Machine.name == name).one()
