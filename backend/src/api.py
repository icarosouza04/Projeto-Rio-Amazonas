import logging
from datetime import datetime, timedelta, date

import pandas as pd
import requests
from backend.src.config import TIMEOUT, VAZAO_MINIMA, SACE_BASE_URL

logger = logging.getLogger(__name__)

FLOOD_URL = "https://flood-api.open-meteo.com/v1/flood"


# ─────────────────────────────────────────────────────────────────────────────
# FONTE PRIMÁRIA: SACE/SGB — cotas reais a cada 15 minutos
# URL: {SACE_BASE_URL}/{bacia}_{pm}_cota.csv
# Coluna "indice" vem em centímetros → dividir por 100 = metros
# ─────────────────────────────────────────────────────────────────────────────

def buscar_cota_sace(bacia, pm, dias=None):
    """
    Baixa o CSV de cotas reais do SACE/SGB.
    Retorna DataFrame com colunas: data, cota_m
    Agrega por dia (média diária das leituras de 15 em 15 min).
    """
    if dias is None:
        from backend.src.config import DIAS_ANALISE
        dias = DIAS_ANALISE

    url = f"{SACE_BASE_URL}/{bacia}_{pm}_cota.csv"
    logger.info(f"Buscando SACE: {url}")

    try:
        resp = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()

        # CSV usa ; como separador
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), sep=";")

        # Renomeia colunas para padrão interno
        df.columns = ["data_hora", "indice"]

        # Converte tipos
        df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
        df["indice"]    = pd.to_numeric(df["indice"], errors="coerce")
        df = df.dropna()

        # Filtra últimos N dias
        limite = datetime.today() - timedelta(days=dias)
        df = df[df["data_hora"] >= limite]

        if df.empty:
            logger.warning(f"SACE sem dados nos últimos {dias} dias: {url}")
            return pd.DataFrame()

        # Converte centímetros → metros
        df["cota_m"] = df["indice"] / 100.0

        # Agrega por dia (média diária)
        df["data"] = df["data_hora"].dt.date
        df_dia = (
            df.groupby("data")["cota_m"]
            .mean()
            .reset_index()
        )
        df_dia["cota_m"] = df_dia["cota_m"].round(2)

        logger.info(f"SACE OK: {len(df_dia)} dias | último={df_dia['data'].max()} | cota={df_dia['cota_m'].iloc[-1]}m")
        return df_dia.reset_index(drop=True)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout SACE: {url}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erro SACE {url}: {e}")
        return pd.DataFrame()


def buscar_cota_sace_horaria(bacia, pm, horas=48):
    """
    Retorna leituras horárias (sem agregar por dia).
    Útil para gráficos de curto prazo / tempo real.
    """
    url = f"{SACE_BASE_URL}/{bacia}_{pm}_cota.csv"
    try:
        resp = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()

        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), sep=";")
        df.columns = ["data_hora", "indice"]
        df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
        df["indice"]    = pd.to_numeric(df["indice"], errors="coerce")
        df = df.dropna()

        limite = datetime.now() - timedelta(hours=horas)
        df = df[df["data_hora"] >= limite]
        df["cota_m"] = df["indice"] / 100.0

        return df[["data_hora", "cota_m"]].reset_index(drop=True)
    except Exception as e:
        logger.error(f"Erro SACE horário: {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────────────────────────────────────────
# FONTE SECUNDÁRIA (fallback): Open-Meteo — vazão modelada
# ─────────────────────────────────────────────────────────────────────────────

def buscar_open_meteo(lat, lon, dias=None, q_min=None):
    """Busca descarga fluvial modelada no Open-Meteo (fallback)."""
    if q_min is None:
        q_min = VAZAO_MINIMA
    if dias is None:
        from backend.src.config import DIAS_ANALISE
        dias = DIAS_ANALISE

    hoje   = datetime.today().date()
    inicio = (hoje - timedelta(days=dias - 1)).isoformat()
    fim    = hoje.isoformat()

    params = {
        "latitude":   lat,
        "longitude":  lon,
        "daily":      "river_discharge",
        "start_date": inicio,
        "end_date":   fim,
    }

    logger.info(f"Buscando Open-Meteo (fallback): lat={lat}, lon={lon}")

    try:
        response = requests.get(FLOOD_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        daily     = data.get("daily", {})
        time      = daily.get("time", [])
        discharge = daily.get("river_discharge", [])

        if not time or not discharge:
            logger.warning(f"Open-Meteo sem dados: lat={lat}, lon={lon}")
            return pd.DataFrame()

        df = pd.DataFrame({
            "data":  pd.to_datetime(time).to_series().dt.date,
            "vazao": [float(v) if v is not None else None for v in discharge],
        })

        df = df.dropna(subset=["vazao"])

        if q_min and q_min > 0:
            df = df[df["vazao"] >= q_min]

        logger.info(f"Open-Meteo OK: {len(df)} registros")
        return df.reset_index(drop=True)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout Open-Meteo lat={lat}, lon={lon}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erro Open-Meteo: {e}")
        return pd.DataFrame()

