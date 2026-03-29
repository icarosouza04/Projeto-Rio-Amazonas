import pandas as pd
import json
import logging
from pathlib import Path
import sys

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config import ESTACOES, CAMINHO_FALLBACK
from api import buscar_open_meteo
from processamento import vazao_para_cota

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def carregar_fallback(estacao):
    """Carrega dados de fallback do arquivo JSON"""
    if not Path(CAMINHO_FALLBACK).exists():
        logger.warning(f"Arquivo de fallback não encontrado: {CAMINHO_FALLBACK}")
        return pd.DataFrame()

    try:
        with open(CAMINHO_FALLBACK, 'r', encoding='utf-8') as f:
            fallback_data = json.load(f)
            if estacao in fallback_data:
                logger.info(f"Carregando fallback para {estacao}")
                df = pd.DataFrame(fallback_data[estacao])
                if 'data' in df.columns:
                    df['data'] = pd.to_datetime(df['data']).dt.date
                return df
            else:
                logger.warning(f"Estação {estacao} não encontrada em fallback")
    except Exception as e:
        logger.error(f"Erro ao carregar fallback: {e}")

    return pd.DataFrame()

def salvar_fallback(dados_api):
    """Salva dados em arquivo fallback JSON"""
    try:
        fallback_dict = {}
        for estacao, df in dados_api.items():
            if not df.empty:
                fallback_dict[estacao] = df.to_dict('records')
        
        Path(CAMINHO_FALLBACK).parent.mkdir(parents=True, exist_ok=True)
        with open(CAMINHO_FALLBACK, 'w', encoding='utf-8') as f:
            json.dump(fallback_dict, f, indent=2, default=str)
        logger.info("Dados salvos em fallback.json")
    except Exception as e:
        logger.error(f"Erro ao salvar fallback: {e}")

def obter_dados_com_fallback(nome, cfg):
    """Tenta dados da API e, se falhar, carrega fallback do json."""
    try:
        df_vazao = buscar_open_meteo(cfg['lat'], cfg['lon'])
        if df_vazao.empty:
            raise ValueError('Dados API vazios')

        logger.info(f"Dados obtidos da API para {nome}.")
        return df_vazao, 'api'

    except Exception as e:
        logger.warning(f"Falha API para {nome} ({e}), tentando fallback")

        df_vazao = carregar_fallback(nome)
        if df_vazao.empty:
            logger.warning(f"Fallback vazio para {nome}")
        else:
            logger.info(f"Dados obtidos do fallback para {nome}.")

        return df_vazao, 'fallback'


def main():
    """Busca dados fluviométricos do Rio Amazonas"""
    dados_api = {}

    for nome, cfg in ESTACOES.items():
        print(f"📡 Buscando dados de {nome}...")
        logger.info(f"Processando estação: {nome}")

        df_vazao, fonte = obter_dados_com_fallback(nome, cfg)

        if not df_vazao.empty:
            df = vazao_para_cota(
                df_vazao,
                cfg['rc_a'],
                cfg['rc_b'],
                cfg['cota_maxima']
            )
            print(f"✅ {len(df)} registros obtidos de {nome} ({fonte})")

        else:
            df = pd.DataFrame()
            print(f"❌ Sem dados para {nome} mesmo após fallback")
            logger.error(f"Não há dados para {nome} na API nem no fallback")

        dados_api[nome] = df

    # Salvar dados para próximas execuções
    if dados_api:
        salvar_fallback(dados_api)

    print("✅ Finalizado!")
    return dados_api

if __name__ == "__main__":
    main()