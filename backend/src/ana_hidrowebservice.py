"""
backend/src/ana_hidrowebservice.py
Integração com a API REST da ANA HidroWebService.
Token dura 60 min — gerenciado aqui automaticamente.
"""

import logging
import time
from datetime import datetime, timedelta

import requests
import pandas as pd

from backend.src.config import ANA_BASE_URL, ANA_CPF_CNPJ, ANA_SENHA, TIMEOUT

logger = logging.getLogger(__name__)

# ── Token em memória ──────────────────────────────────────────────────────────
_token: str = ""
_token_expira: float = 0.0


def _autenticar() -> str:
    global _token, _token_expira
    if _token and time.time() < _token_expira:
        return _token

    url = f"{ANA_BASE_URL}/OAut/Token"
    try:
        resp = requests.post(
            url,
            json={"cpfCnpj": ANA_CPF_CNPJ, "senha": ANA_SENHA},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        _token = data["token"]
        _token_expira = time.time() + 55 * 60   # renova antes dos 60 min
        logger.info("ANA HidroWS: autenticado ✓")
        return _token
    except Exception as e:
        logger.error(f"ANA autenticação falhou: {e}")
        raise


def buscar_cota_ana_adotada(codigo_estacao: str, dias: int = 30) -> pd.DataFrame:
    """
    Retorna DataFrame com colunas: data (date), cota_m (float).
    Usa a cota adotada diária da estação ANA.
    """
    token = _autenticar()

    fim    = datetime.today().date()
    inicio = fim - timedelta(days=dias - 1)

    url = f"{ANA_BASE_URL}/Cotas/CotaAdotada"
    headers = {"Authorization": f"Bearer {token}"}
    params  = {
        "codEstacao":  codigo_estacao,
        "dataInicio":  inicio.strftime("%Y-%m-%d"),
        "dataFim":     fim.strftime("%Y-%m-%d"),
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        itens = resp.json()          # lista de dicts

        if not itens:
            return pd.DataFrame()

        df = pd.DataFrame(itens)

        # Normaliza nomes de campo — a ANA usa diferentes nomes em versões
        col_data = next((c for c in df.columns if "data" in c.lower()), None)
        col_cota = next((c for c in df.columns if "cota" in c.lower()), None)

        if not col_data or not col_cota:
            logger.warning(f"ANA: colunas inesperadas {list(df.columns)}")
            return pd.DataFrame()

        df = df.rename(columns={col_data: "data", col_cota: "cota_cm"})
        df["data"]   = pd.to_datetime(df["data"]).dt.date
        df["cota_cm"] = pd.to_numeric(df["cota_cm"], errors="coerce")
        df = df.dropna(subset=["cota_cm"])
        df["cota_m"] = (df["cota_cm"] / 100.0).round(2)

        df = df[["data", "cota_m"]].sort_values("data").reset_index(drop=True)
        logger.info(f"ANA [{codigo_estacao}]: {len(df)} registros | último {df['data'].max()}")
        return df

    except Exception as e:
        logger.error(f"ANA buscar_cota [{codigo_estacao}]: {e}")
        return pd.DataFrame()


def listar_estacoes_amazonas() -> pd.DataFrame:
    """Utilitário: lista estações ANA no estado do Amazonas (UF=AM)."""
    token = _autenticar()
    url = f"{ANA_BASE_URL}/Estacoes/ListaEstacoes"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"codUf": "AM", "tipoEstacao": "1"}   # tipo 1 = fluviométrica
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        return pd.DataFrame(resp.json())
    except Exception as e:
        logger.error(f"ANA listar_estacoes: {e}")
        return pd.DataFrame()
