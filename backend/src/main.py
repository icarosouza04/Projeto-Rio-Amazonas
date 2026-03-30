import pandas as pd
import json
import logging
from pathlib import Path

from backend.src.config import ESTACOES, CAMINHO_FALLBACK
from backend.src.api import buscar_open_meteo
from backend.src.processamento import vazao_para_cota

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


def calcular_tendencia_mensal(df):
    if df.empty:
        return {}

    monthly = (
        df.assign(data=pd.to_datetime(df['data']))
          .assign(mes=lambda x: x['data'].dt.strftime('%b'))
          .groupby('mes')['cota_m']
          .mean()
          .reindex(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'])
    )

    monthly = monthly.dropna().to_dict()
    return {mes: round(float(valor), 2) for mes, valor in monthly.items()}


def montar_resposta(df, fonte):
    if df.empty:
        return {'dados': [], 'fonte': fonte, 'tendencia_mensal': {}}

    normalizado = []
    df = df.sort_values('data').reset_index(drop=True)

    for _, row in df.iterrows():
        normalizado.append({
            'data': pd.to_datetime(row['data']).date().isoformat(),
            'vazao': float(row['vazao']) if pd.notna(row.get('vazao')) else None,
            'cota_m': float(row['cota_m']) if pd.notna(row.get('cota_m')) else None
        })

    return {
        'dados': normalizado,
        'fonte': fonte,
        'tendencia_mensal': calcular_tendencia_mensal(df)
    }


def obter_dados():
    """Retorna dados para todas as estações."""
    resposta = {}

    for nome, cfg in ESTACOES.items():
        df_vazao, fonte = obter_dados_com_fallback(nome, cfg)

        if not df_vazao.empty:
            df_cota = vazao_para_cota(df_vazao, cfg['rc_a'], cfg['rc_b'], cfg['cota_maxima'])
        else:
            df_cota = pd.DataFrame()

        resposta[nome] = montar_resposta(df_cota, fonte)

    # Salva fallback sempre que houver dados novos
    fallback_para_salvar = {}
    for nome, info in resposta.items():
        if info['dados']:
            fallback_para_salvar[nome] = pd.DataFrame(info['dados'])
        else:
            fallback_para_salvar[nome] = pd.DataFrame()

    salvar_fallback(fallback_para_salvar)

    return resposta


def main():
    """Busca dados fluviométricos do Rio Amazonas"""
    resultado = obter_dados()
    print("✅ Processo concluído")
    return resultado


if __name__ == '__main__':
    main()