from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from lighthouse.db import Base


class Port(Base):
    __tablename__ = 'port'

    number = Column(Integer, primary_key=True)
    machine_id = Column(UUID(as_uuid=True), ForeignKey('machine.id'),
                        primary_key=True)
    forwarded = Column(Boolean, default=False, nullable=False)

    machine = relationship('Machine', single_parent=True,
                           back_populates='ports')
