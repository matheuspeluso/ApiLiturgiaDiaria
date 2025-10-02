# models/entities/Liturgia.py
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date

class LiturgiaDiaria(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    primeiraLeitura: str
    salmoResponsorial: str
    segundaLeitura: str  
    evangelho: str
    data: date