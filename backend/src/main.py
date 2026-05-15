"""
backend/src/main.py  — atualizado com ANA na cadeia de fallback

NOVA HIERARQUIA DE FONTES:
  1. SACE/SGB    → cotas reais a cada 15min (para estações com sace_bacia)
  2. ANA HidroWS → cotas reais a cada 15min (para TODAS as estações, se credenciais configuradas)
  3. Open-Meteo  → vazão modelada convertida em cota estimada
  4. Fallback local JSON

PARA ATIVAR A ANA:
  Adicione no seu .env:
    ANA_CPF_CNPJ=seu_cpf_ou_cnpj
    ANA_SENHA=sua_senha
"""

import pandas as pd
import json
import logging
from pathlib import Path

from backend.src.config import ESTACOES, CAMINHO_FALLBACK, ANA_CPF_CNPJ
from backend.src.api import buscar_cota_sace, buscar_open_meteo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Importa ANA apenas se credenciais estiverem configuradas
_ANA_DISPONIVEL = bool(ANA_CPF_CNPJ)
if _ANA_DISPONIVEL:
    try:
        from backend.src.ana_hidrowebservice import buscar_cota_ana_adotada
        logger.info("ANA HidroWebService: credenciais encontradas, fonte habilitada ✓")
    except ImportError:
        _ANA_DISPONIVEL = False
        logger.warning("ANA HidroWebService: módulo não encontrado (ana_hidrowebservice.py)")
else:
    logger.info("ANA HidroWebService: sem credenciais, usando SACE + Open-Meteo")


# ─────────────────────────────────────────────────────────────────────────────
# Funções auxiliares (sem alteração)
# ─────────────────────────────────────────────────────────────────────────────

def carregar_fallback(estacao):
    if not Path(CAMINHO_FALLBACK).exists():
        return pd.DataFrame()
    try:
        with open(CAMINHO_FALLBACK, "r", encoding="utf-8") as f:
            fb = json.load(f)
            if estacao in fb:
                df = pd.DataFrame(fb[estacao])
                if "data" in df.columns:
                    df["data"] = pd.to_datetime(df["data"]).dt.date
                return df
    except Exception as e:
        logger.error(f"Erro ao carregar fallback: {e}")
    return pd.DataFrame()


def salvar_fallback(dados_api):
    try:
        fallback_dict = {}
        for estacao, df in dados_api.items():
            if not df.empty:
                fallback_dict[estacao] = df.to_dict("records")
        Path(CAMINHO_FALLBACK).parent.mkdir(parents=True, exist_ok=True)
        with open(CAMINHO_FALLBACK, "w", encoding="utf-8") as f:
            json.dump(fallback_dict, f, indent=2, default=str)
        logger.info("Fallback salvo.")
    except Exception as e:
        logger.error(f"Erro ao salvar fallback: {e}")


def normalizar_vazao(series):
    vmin, vmax = series.min(), series.max()
    if vmax == vmin:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - vmin) / (vmax - vmin)


def vazao_para_cota_real(df_vazao, cfg):
    df = df_vazao.copy()
    cota_min  = cfg["cota_min_hist"]
    cota_max  = cfg["cota_max_hist"]
    amplitude = cota_max - cota_min
    norm = normalizar_vazao(df["vazao"])
    df["cota_m"] = cota_min + amplitude * (norm ** 0.55)
    df["cota_m"] = df["cota_m"].clip(upper=cota_max)
    return df


def calcular_tendencia_mensal(df):
    if df.empty or "cota_m" not in df.columns:
        return {}
    try:
        monthly = (
            df.assign(data=pd.to_datetime(df["data"]))
              .assign(mes=lambda x: x["data"].dt.strftime("%b"))
              .groupby("mes")["cota_m"]
              .mean()
              .reindex(["Jan","Fev","Mar","Abr","Mai","Jun",
                        "Jul","Ago","Set","Out","Nov","Dez"])
        )
        monthly = monthly.dropna().to_dict()
        return {mes: round(float(v), 2) for mes, v in monthly.items()}
    except Exception as e:
        logger.error(f"Erro tendência mensal: {e}")
        return {}


def montar_resposta(df, fonte):
    if df.empty:
        return {"dados": [], "fonte": fonte, "tendencia_mensal": {}}

    df = df.sort_values("data").reset_index(drop=True)
    normalizado = []
    for _, row in df.iterrows():
        normalizado.append({
            "data":   pd.to_datetime(row["data"]).date().isoformat(),
            "vazao":  float(row["vazao"])  if "vazao"  in row and pd.notna(row.get("vazao"))  else None,
            "cota_m": float(row["cota_m"]) if "cota_m" in row and pd.notna(row.get("cota_m")) else None,
        })

    return {
        "dados": normalizado,
        "fonte": fonte,
        "tendencia_mensal": calcular_tendencia_mensal(df),
    }


# ─────────────────────────────────────────────────────────────────────────────
# NOVA HIERARQUIA: SACE → ANA → Open-Meteo → Fallback local
# ─────────────────────────────────────────────────────────────────────────────

def obter_dados_com_fallback(nome, cfg):
    """
    Hierarquia de fontes:
    1. SACE/SGB  → cotas reais (cm → m), atualização a cada 15 min
    2. ANA HidroWS → cotas reais (cm → m), até 30 dias, se credenciais OK
    3. Open-Meteo → vazão modelada convertida em cota estimada
    4. Fallback local (JSON salvo da última consulta bem-sucedida)
    """

    # ── 1. Tenta SACE (fonte primária para estações mapeadas) ──────────────
    if cfg.get("sace_bacia") and cfg.get("sace_pm") is not None:
        try:
            df_sace = buscar_cota_sace(cfg["sace_bacia"], cfg["sace_pm"])
            if not df_sace.empty:
                logger.info(f"[{nome}] Fonte: SACE ✓")
                return df_sace, "sace"
            logger.warning(f"[{nome}] SACE retornou vazio")
        except Exception as e:
            logger.warning(f"[{nome}] SACE falhou ({e})")

    # ── 2. Tenta ANA HidroWebService (para TODAS as estações) ─────────────
    if _ANA_DISPONIVEL and cfg.get("codigo_ana"):
        try:
            df_ana = buscar_cota_ana_adotada(
                codigo_estacao=str(cfg["codigo_ana"]),
                dias=30,
            )
            if not df_ana.empty:
                logger.info(f"[{nome}] Fonte: ANA HidroWS ✓")
                return df_ana, "ana"
            logger.warning(f"[{nome}] ANA retornou vazio")
        except Exception as e:
            logger.warning(f"[{nome}] ANA falhou ({e})")

    # ── 3. Tenta Open-Meteo (estimativa por vazão modelada) ────────────────
    try:
        df_vazao = buscar_open_meteo(cfg["lat"], cfg["lon"])
        if not df_vazao.empty:
            df_cota = vazao_para_cota_real(df_vazao, cfg)
            logger.info(f"[{nome}] Fonte: Open-Meteo (estimativa)")
            return df_cota, "open-meteo"
        raise ValueError("Open-Meteo retornou vazio")
    except Exception as e:
        logger.warning(f"[{nome}] Open-Meteo falhou ({e}), usando fallback local")

    # ── 4. Fallback local ──────────────────────────────────────────────────
    df = carregar_fallback(nome)
    logger.info(f"[{nome}] Fonte: fallback local")
    return df, "fallback"


def obter_dados():
    resposta = {}

    for nome, cfg in ESTACOES.items():
        df, fonte = obter_dados_com_fallback(nome, cfg)

        if not df.empty and "cota_m" not in df.columns:
            if "vazao" in df.columns:
                df = vazao_para_cota_real(df, cfg)

        resposta[nome] = montar_resposta(df, fonte)

    # Salva fallback com dados novos
    para_salvar = {}
    for nome, info in resposta.items():
        if info["dados"]:
            para_salvar[nome] = pd.DataFrame(info["dados"])
        else:
            para_salvar[nome] = pd.DataFrame()
    salvar_fallback(para_salvar)

    return resposta


def main():
    resultado = obter_dados()
    for nome, info in resultado.items():
        d = info["dados"]
        ult = d[-1] if d else {}
        logger.info(
            f"{nome}: {len(d)} registros | "
            f"cota={ult.get('cota_m','—')}m | "
            f"fonte={info['fonte']}"
        )
    return resultado


if __name__ == "__main__":
    main()
