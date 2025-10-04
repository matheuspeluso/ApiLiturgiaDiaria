import requests
from bs4 import BeautifulSoup
from datetime import date
from sqlalchemy.orm import Session
from models.dtos.LiturgiaDto import LiturgiaDiaria
from infrastructure.repositories import liturgiaRepository

def liturgiaScrapService() -> LiturgiaDiaria:
    urlsite = 'https://liturgia.cancaonova.com/pb/'

    try:
        response = requests.get(urlsite, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Erro ao acessar o site: {e}")

    parsed_html = BeautifulSoup(response.text, 'html.parser')

    title = parsed_html.title.string if parsed_html.title else "Sem título"
    print(f"Página carregada: {title}")

    primeira_leitura_elem = parsed_html.select_one('#liturgia-1')
    salmo_elem = parsed_html.select_one('#liturgia-2')
    segunda_leitura_elem = parsed_html.select_one('#liturgia-3')
    evangelho_elem = parsed_html.select_one('#liturgia-4')

    primeira_leitura = primeira_leitura_elem.get_text(strip=True) if primeira_leitura_elem else "Não disponível"
    salmo = salmo_elem.get_text(strip=True) if salmo_elem else "Não disponível"
    segunda_leitura = segunda_leitura_elem.get_text(strip=True) if segunda_leitura_elem else "Não disponível"
    evangelho = evangelho_elem.get_text(strip=True) if evangelho_elem else "Não disponível"

    print(f"Primeira leitura (trecho): {primeira_leitura[:60]}...")

    return LiturgiaDiaria(
        primeiraLeitura=primeira_leitura,
        salmoResponsorial=salmo,
        segundaLeitura=segunda_leitura,
        evangelho=evangelho,
        data=date.today()
    )

def salvar_liturgia(db: Session) -> dict:
    hoje = date.today()
    liturgia_existente = liturgiaRepository.get_liturgia_by_date(db, hoje)
    if liturgia_existente:
        return {
            "message": "Liturgia do dia já existe no banco",
            "id": liturgia_existente.id,
            "data": str(hoje)
        }

    liturgia_dto = liturgiaScrapService()
    liturgia = liturgiaRepository.save_liturgia(db, liturgia_dto)
    return {
        "message": "Liturgia salva com sucesso",
        "id": liturgia.id,
        "data": str(liturgia.data)
    }

def buscar_todas_liturgias(db: Session):
    return liturgiaRepository.get_all_liturgias(db)

def buscar_liturgia_pelo_id(db: Session, liturgia_id):
    return liturgiaRepository.get_liturgia_by_id(db, liturgia_id)