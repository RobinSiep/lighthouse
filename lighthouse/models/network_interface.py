from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from lighthouse.db import Base
from lighthouse.lib.network import (
    get_subnet_size, network_addr_to_binary_string)


class NetworkInterface(Base):
    __tablename__ = 'network_interface'

    name = Column(String(64), primary_key=True)
    machine_id = Column(UUID(as_uuid=True), ForeignKey('machine.id'),
                        primary_key=True)
    ip_address = Column(String(16), nullable=False)
    netmask = Column(String(16), nullable=False)

    machine = relationship('Machine', single_parent=True,
                           back_populates='network_interfaces')

    @property
    def subnet_addr(self):
        subnet_size = get_subnet_size(self.netmask)
        return network_addr_to_binary_string(
            self.ip_address)[:32-(32-subnet_size)]
