from datetime import date, timedelta
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.src.main import obter_dados, calcular_tendencia_mensal
from backend.src.config import ESTACOES
# ← NOVO: importa busca horária do SACE
from backend.src.api import buscar_cota_sace_horaria

app = FastAPI(title="Rio Amazonas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dados")
async def get_dados(
    estacao: Optional[str] = None,
    dias: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
):
    resultado = obter_dados()

    if estacao:
        if estacao not in resultado:
            raise HTTPException(status_code=404, detail=f"Estação '{estacao}' não encontrada")
        resultados = {estacao: resultado[estacao]}
    else:
        resultados = resultado

    def filtrar_entrada(registro):
        if not registro:
            return registro
        dados = registro.get('dados', [])
        if not dados:
            return registro

        end_date = None
        start_date = None

        if dias is not None and dias > 0:
            end_date = date.today()
            start_date = end_date - timedelta(days=dias - 1)

        if data_inicio is not None:
            start_date = data_inicio if start_date is None else min(start_date, data_inicio)

        if data_fim is not None:
            end_date = data_fim if end_date is None else max(end_date, data_fim)

        if start_date or end_date:
            filtrado = []
            for item in dados:
                try:
                    item_date = date.fromisoformat(item.get('data'))
                except Exception:
                    continue
                if start_date and item_date < start_date:
                    continue
                if end_date and item_date > end_date:
                    continue
                filtrado.append(item)
            dados = filtrado

        df = pd.DataFrame(dados) if dados else pd.DataFrame()
        return {
            'dados': dados,
            'fonte': registro.get('fonte', 'desconhecido'),
            'tendencia_mensal': calcular_tendencia_mensal(df) if not df.empty else {}
        }

    for nome, registro in list(resultados.items()):
        resultados[nome] = filtrar_entrada(registro)

    return resultados


# ── NOVO: cota atual em tempo real (últimas 48h, leitura a cada 15min) ────────
@app.get("/api/dados/tempo-real")
async def get_tempo_real(estacao: Optional[str] = None, horas: int = 48):
    """
    Retorna leituras horárias direto do SACE (não agrega por dia).
    Ideal para mostrar a cota atual e variação recente no dashboard.
    """
    estacoes_alvo = {}

    if estacao:
        if estacao not in ESTACOES:
            raise HTTPException(status_code=404, detail=f"Estação '{estacao}' não encontrada")
        estacoes_alvo = {estacao: ESTACOES[estacao]}
    else:
        estacoes_alvo = ESTACOES

    resposta = {}
    for nome, cfg in estacoes_alvo.items():
        if not cfg.get("sace_bacia") or cfg.get("sace_pm") is None:
            resposta[nome] = {"dados": [], "fonte": "sem-sace"}
            continue

        df = buscar_cota_sace_horaria(cfg["sace_bacia"], cfg["sace_pm"], horas=horas)

        if df.empty:
            resposta[nome] = {"dados": [], "fonte": "sace-vazio"}
            continue

        leituras = [
            {
                "data_hora": row["data_hora"].isoformat(),
                "cota_m":    round(row["cota_m"], 2),
            }
            for _, row in df.iterrows()
        ]

        # Cota mais recente = última leitura
        cota_atual = leituras[-1]["cota_m"] if leituras else None

        resposta[nome] = {
            "cota_atual": cota_atual,
            "dados":      leituras,
            "fonte":      "sace",
        }

    return resposta


@app.get("/api/estacoes")
async def get_estacoes():
    return {"estacoes": list(ESTACOES.keys())}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
