import logging
from datetime import datetime, timedelta

import pandas as pd
import requests
from backend.src.config import OPEN_METEO_URL, OPEN_METEO_PARAMS, TIMEOUT, VAZAO_MINIMA

logger = logging.getLogger(__name__)

def buscar_open_meteo(lat, lon, dias=None, q_min=None):
    """Busca dados de descarga do rio via Open-Meteo API."""
    if q_min is None:
        q_min = VAZAO_MINIMA
    if dias is None:
        from config import DIAS_ANALISE
        dias = DIAS_ANALISE

    hoje = datetime.today().date()
    inicio = (hoje - timedelta(days=dias - 1)).isoformat()
    fim = hoje.isoformat()

    params = {
        **OPEN_METEO_PARAMS,
        "latitude": lat,
        "longitude": lon,
        "start_date": inicio,
        "end_date": fim
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()

        data = response.json()

        # Transformar em DataFrame
        daily = data.get("daily", {})
        time = daily.get("time", [])
        discharge = daily.get("river_discharge", [])

        if not time or not discharge or len(time) != len(discharge):
            logger.warning(f"Resposta da API sem dados esperados para lat={lat}, lon={lon}")
            return pd.DataFrame()

        df = pd.DataFrame({
            "data": pd.to_datetime(time).to_series().dt.date,
            "vazao": discharge
        })

        # Filtrar vazão mínima
        df = df[df["vazao"] >= q_min]
        return df.reset_index(drop=True)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout ao buscar dados (lat={lat}, lon={lon})")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Erro ao processar resposta da API: {e}")
        return pd.DataFrame()