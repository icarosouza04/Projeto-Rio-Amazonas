from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Rio Amazonas API", description="API para dados fluviométricos")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dados mock para teste
DADOS_MOCK = {
    "Manaus": [
        {"data": "2026-03-28", "vazao": 120000.0, "cota_m": 29.5},
        {"data": "2026-03-29", "vazao": 130000.0, "cota_m": 30.1}
    ],
    "Óbidos": [
        {"data": "2026-03-28", "vazao": 90000.0, "cota_m": 6.5},
        {"data": "2026-03-29", "vazao": 95000.0, "cota_m": 6.8}
    ]
}

@app.get("/api/dados")
async def get_dados():
    """Endpoint para obter dados das estações"""
    return DADOS_MOCK

@app.get("/api/estacoes")
async def get_estacoes():
    """Endpoint para obter lista de estações"""
    estacoes = list(DADOS_MOCK.keys())
    return {"estacoes": estacoes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)