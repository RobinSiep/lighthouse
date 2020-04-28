from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from lighthouse.db import Base


class NetworkInterface(Base):
    __tablename__ = 'network_interface'

    name = Column(String(64), primary_key=True)
    machine_id = Column(UUID(as_uuid=True), ForeignKey('machine.id'),
                        primary_key=True)
    ip_address = Column(String(16), nullable=False)
    netmask = Column(String(16), nullable=False)
