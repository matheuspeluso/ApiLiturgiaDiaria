from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from infrastructure.factory.database import get_db
from service import liturgiaService
from typing import List
from models.dtos.LiturgiaDto import LiturgiaDiaria 

app = FastAPI(
    title="Liturgia Diária API",
    description="Essa API faz webscraping no site da Canção Nova e permite salvar/consultar liturgias no banco.",
    version="1.0.0"
)


@app.get("/liturgia/scrap", response_model = LiturgiaDiaria, description = "Faz um Web Scraping no site da canção nova e apenas imprime a liturgia do dia (não salva no banco)", tags=["Web Scraping"])
def read_liturgia_scrap():
    return liturgiaService.liturgiaScrapService()

@app.post("/liturgia" , response_model = LiturgiaDiaria, description = "Faz um Web Scraping no site da canção nova e salva a liturgia do dia no banco, se ainda não existir", tags=["Web Scraping"])
def salvar_liturgia(db: Session = Depends(get_db)):
    return liturgiaService.salvar_liturgia(db)

@app.get("/liturgia", response_model=List[LiturgiaDiaria], description = "Lista todas as liturgias salvas no banco", tags=["Liturgias"])
def listar_liturgias(db: Session = Depends(get_db)):
    liturgiaBanco = liturgiaService.buscar_todas_liturgias(db)
    listaDeLiturgias = [
        LiturgiaDiaria(
            id=liturgia.id,
            primeiraLeitura=liturgia.primeira_leitura,
            salmoResponsorial=liturgia.salmo_responsorial,
            segundaLeitura=liturgia.segunda_leitura,
            evangelho=liturgia.evangelho,
            data=liturgia.data
        )
        for liturgia in liturgiaBanco
    ]
    return listaDeLiturgias

@app.get("/liturgia/{liturgia_id}", response_model=LiturgiaDiaria, description = "Busca uma liturgia específica pelo ID fornecido na URL", tags=["Liturgias"])
def buscar_liturgia_por_id(liturgia_id: str, db: Session = Depends(get_db)):
    liturgia = liturgiaService.buscar_liturgia_pelo_id(db, liturgia_id)
    if liturgia is None:
        return {"message": "Liturgia não encontrada"}
    liturgia_dto = LiturgiaDiaria(
        id=liturgia.id,
        primeiraLeitura=liturgia.primeira_leitura,
        salmoResponsorial=liturgia.salmo_responsorial,
        segundaLeitura=liturgia.segunda_leitura,
        evangelho=liturgia.evangelho,
        data=liturgia.data
    )
    
    return liturgia_dto
    