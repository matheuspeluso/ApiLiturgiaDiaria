import requests
from bs4 import BeautifulSoup
from datetime import date
from models.entities.Liturgia import LiturgiaDiaria

def liturgiaScrapService() -> LiturgiaDiaria:
    urlsite = 'https://liturgia.cancaonova.com/pb/'
    
    try:
        response = requests.get(urlsite, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Erro ao acessar o site: {e}")

    raw_html = response.text
    parsed_html = BeautifulSoup(raw_html, 'html.parser')

    # Seleciona os elementos
    primeira_leitura_elem = parsed_html.select_one('#liturgia-1')
    salmo_elem = parsed_html.select_one('#liturgia-2')
    segunda_leitura_elem = parsed_html.select_one('#liturgia-3')
    evangelho_elem = parsed_html.select_one('#liturgia-4')

    # Extrai texto ou usa fallback
    primeira_leitura = primeira_leitura_elem.get_text(strip=True) if primeira_leitura_elem else "Não disponível"
    salmo = salmo_elem.get_text(strip=True) if salmo_elem else "Não disponível"
    segunda_leitura = segunda_leitura_elem.get_text(strip=True) if segunda_leitura_elem else "Não disponível"
    evangelho = evangelho_elem.get_text(strip=True) if evangelho_elem else "Não disponível"

    # Retorna instância do modelo Pydantic
    return LiturgiaDiaria(
        primeiraLeitura=primeira_leitura,
        salmoResponsorial=salmo,
        segundaLeitura=segunda_leitura,
        evangelho=evangelho,
        data=date.today()
    )