import uuid

from sqlalchemy import Column, String

from lighthousemaster.db import Base, DBSession as session


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), unique=True, nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)


def list_machines():
    return session.query(Machine).all()
