from datetime import date, timedelta
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.src.main import obter_dados, calcular_tendencia_mensal
from backend.src.config import ESTACOES

app = FastAPI(title="Rio Amazonas API", description="API para dados fluviométricos")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_default_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.get("/api/dados")
async def get_dados(estacao: Optional[str] = None, dias: Optional[int] = None, data_inicio: Optional[date] = None, data_fim: Optional[date] = None):
    """Endpoint para obter dados das estações."""
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

        # Preparar período de filtro
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

        return {
            'dados': dados,
            'fonte': registro.get('fonte', 'desconhecido'),
            'tendencia_mensal': calcular_tendencia_mensal(
                pd.DataFrame(dados) if dados else pd.DataFrame()
            ) if dados else {}
        }

    # Import local pandas to avoid heavier dependency only in this endpoint
    import pandas as pd

    for nome, registro in list(resultados.items()):
        resultados[nome] = filtrar_entrada(registro)

    return resultados

@app.get("/api/estacoes")
async def get_estacoes():
    """Endpoint para obter lista de estações"""
    return {"estacoes": list(ESTACOES.keys())}

@app.get("/api/estacoes")
async def get_estacoes():
    """Endpoint para obter lista de estações"""
    return {"estacoes": list(ESTACOES.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)