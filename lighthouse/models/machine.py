import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from lighthouse.db import Base, DBSession as session


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sid = Column(String(32), unique=True, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)
    external_ip = Column(String(32), nullable=False)

    def set_fields(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def list_machines():
    return session.query(Machine).all()


def get_machine_by_id(id_):
    return session.query(Machine).get(id_)


def get_machine_by_name(name):
    return session.query(Machine).filter(Machine.name == name).one()


def get_machine_by_mac_address(mac_address):
    return session.query(Machine).filter(
        Machine.mac_address == mac_address
    ).one()
