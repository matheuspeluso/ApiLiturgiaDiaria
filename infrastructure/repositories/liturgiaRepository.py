from sqlalchemy.orm import Session
from models.entities.Liturgia import Liturgia
from models.dtos.LiturgiaDto import LiturgiaDiaria
from uuid import uuid4, UUID as uuid

def save_liturgia(db: Session, liturgia_dto: LiturgiaDiaria) -> Liturgia:
    liturgia = Liturgia(
        primeira_leitura=liturgia_dto.primeiraLeitura,
        salmo_responsorial=liturgia_dto.salmoResponsorial,
        segunda_leitura=liturgia_dto.segundaLeitura,
        evangelho=liturgia_dto.evangelho,
        data=liturgia_dto.data,
    )
    db.add(liturgia)
    db.commit()
    db.refresh(liturgia)
    print(f"✅ Liturgia salva no banco com ID: {liturgia.id}")
    return liturgia

def get_all_liturgias(db: Session) -> list[Liturgia]:
    result = db.query(Liturgia).all()
    print(f"🔍 Total de liturgias no banco: {len(result)}")
    return result

def get_liturgia_by_date(db: Session, data) -> Liturgia | None:
    return db.query(Liturgia).filter(Liturgia.data == data).first()

def get_liturgia_by_id(db: Session, liturgia_id: uuid) -> Liturgia | None:
    return db.query(Liturgia).filter(Liturgia.id == liturgia_id).first()