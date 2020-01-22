from lighthousemaster.db import Base

from sqlalchemy import Column, String


class Machine(Base):
    __tablename__ = 'machine'

    id = Column(String(32), primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)
