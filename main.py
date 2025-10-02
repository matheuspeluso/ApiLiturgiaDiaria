from fastapi import FastAPI
from datetime import date
from models.entities.Liturgia import LiturgiaDiaria
from service.liturgiaService import liturgiaScrapService

# ✅ Primeiro: cria a app
app = FastAPI(
    title="Liturgia Diária API",
    description="Essa api faz um webscraping no site da Canção Nova e retorna a liturgia do dia.",
    version="1.0.0"
)

# ✅ Depois: define as rotas
@app.get("/liturgia")
def read_liturgia():
    try:
        liturgia = liturgiaScrapService()
        return liturgia
    except Exception as e:
        return {"error": str(e)}
