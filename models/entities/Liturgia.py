from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from infrastructure.factory.database import Base

class Liturgia(Base):
    __tablename__ = "liturgias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    primeira_leitura = Column(String, nullable=False)
    salmo_responsorial = Column(String, nullable=False)
    segunda_leitura = Column(String, nullable=True)
    evangelho = Column(String, nullable=False)
    data = Column(Date, nullable=False, unique=True)
