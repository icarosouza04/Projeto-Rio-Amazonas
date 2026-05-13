"""
FluviAM — config.py  (v4.2)
============================

SACE/SGB IDs mapeados:
  amazonas_8   → Manaus
  amazonas_12  → Manacapuru
  amazonas_26  → Itacoatiara
  amazonas_15  → Tabatinga
  amazonas_34  → Óbidos
  amazonas_19  → Beruri

Estações sem SACE → ANA (se credenciais configuradas) → TelWS1 → Open-Meteo

Credenciais ANA via variáveis de ambiente:
  ANA_CPF_CNPJ=seu_cpf_ou_cnpj
  ANA_SENHA=sua_senha
"""

from pathlib import Path
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── GERAL ─────────────────────────────────────────────────────────────────────
TIMEOUT      = 20
DIAS_ANALISE = 60
VAZAO_MINIMA = 0

# ── SACE/SGB ──────────────────────────────────────────────────────────────────
SACE_BASE_URL = "https://www.sgb.gov.br/sace/sace_nivel/api/dados"

# ── ANA HidroWebService ───────────────────────────────────────────────────────
ANA_BASE_URL = "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas"
ANA_CPF_CNPJ = os.getenv("ANA_CPF_CNPJ", "")
ANA_SENHA    = os.getenv("ANA_SENHA",    "")
ANA_LOGIN    = ANA_CPF_CNPJ
ANA_PASSWORD = ANA_SENHA

# ── HidroWeb REST ─────────────────────────────────────────────────────────────
HIDROWEB_TOKEN = os.getenv("HIDROWEB_TOKEN", "")

# ── Open-Meteo ────────────────────────────────────────────────────────────────
FLOOD_URL = "https://flood-api.open-meteo.com/v1/flood"

# ── ESTAÇÕES ──────────────────────────────────────────────────────────────────
ESTACOES = {

    # ── COM SACE ─────────────────────────────────────────────────────────────

    "Manaus": {
        "codigo": "14990000", "codigo_ana": "14990000",
        "lat": -3.10, "lon": -60.02, "rio": "Rio Negro",
        "cota_atual_ref": 26.56, "cota_max_hist": 29.97, "cota_min_hist": 12.11,
        "cota_media": 22.50, "cota_alerta": 29.00, "cota_atencao": 20.30,
        "cota_emergencia": 34.80, "cota_maxima": 29.97,
        "sace_bacia": "amazonas", "sace_pm": 8,
    },

    "Manacapuru": {
        "codigo": "13850000", "codigo_ana": "13850000",
        "lat": -3.31, "lon": -60.61, "rio": "Rio Solimões",
        "cota_atual_ref": 18.00, "cota_max_hist": 23.50, "cota_min_hist": 3.20,
        "cota_media": 15.00, "cota_alerta": 21.00, "cota_atencao": 14.70,
        "cota_emergencia": 25.20, "cota_maxima": 23.50,
        "sace_bacia": "amazonas", "sace_pm": 12,
    },

    "Itacoatiara": {
        "codigo": "14280000", "codigo_ana": "14280000",
        "lat": -3.14, "lon": -58.44, "rio": "Rio Amazonas",
        "cota_atual_ref": 13.00, "cota_max_hist": 16.83, "cota_min_hist": 1.20,
        "cota_media": 9.50, "cota_alerta": 14.00, "cota_atencao": 9.80,
        "cota_emergencia": 16.80, "cota_maxima": 16.83,
        "sace_bacia": "amazonas", "sace_pm": 26,
    },

    "Tabatinga": {
        "codigo": "13020000", "codigo_ana": "13020000",
        "lat": -4.25, "lon": -69.94, "rio": "Rio Solimões",
        "cota_atual_ref": 11.10, "cota_max_hist": 13.50, "cota_min_hist": -2.34,
        "cota_media": 7.50, "cota_alerta": 11.00, "cota_atencao": 7.70,
        "cota_emergencia": 13.20, "cota_maxima": 13.50,
        "sace_bacia": "amazonas", "sace_pm": 15,
    },

    "Óbidos": {
        "codigo": "17050001", "codigo_ana": "17050001",
        "lat": -1.92, "lon": -55.52, "rio": "Rio Amazonas",
        "cota_atual_ref": 8.50, "cota_max_hist": 11.20, "cota_min_hist": -2.53,
        "cota_media": 5.80, "cota_alerta": 9.00, "cota_atencao": 6.30,
        "cota_emergencia": 10.80, "cota_maxima": 11.20,
        "sace_bacia": "amazonas", "sace_pm": 34,
    },

    "Beruri": {
        "codigo": "13762000", "codigo_ana": "13762000",
        "lat": -3.90, "lon": -61.28, "rio": "Rio Purus",
        "cota_atual_ref": 10.00, "cota_max_hist": 15.80, "cota_min_hist": 1.50,
        "cota_media": 8.50, "cota_alerta": 13.50, "cota_atencao": 9.20,
        "cota_emergencia": 15.50, "cota_maxima": 15.80,
        "sace_bacia": "amazonas", "sace_pm": 19,
    },

    # ── SEM SACE — ANA → TelWS1 → Open-Meteo ─────────────────────────────────

    "Parintins": {
        "codigo": "14540000", "codigo_ana": "14540000",
        "lat": -2.63, "lon": -56.74, "rio": "Rio Amazonas",
        "cota_atual_ref": 10.50, "cota_max_hist": 13.80, "cota_min_hist": -1.76,
        "cota_media": 7.20, "cota_alerta": 11.50, "cota_atencao": 8.05,
        "cota_emergencia": 13.80, "cota_maxima": 13.80,
        "sace_bacia": None, "sace_pm": None,
    },

    "Tefé": {
        "codigo": "13760000", "codigo_ana": "13760000",
        "lat": -3.37, "lon": -64.72, "rio": "Rio Solimões",
        "cota_atual_ref": 12.00, "cota_max_hist": 17.50, "cota_min_hist": 1.46,
        "cota_media": 10.20, "cota_alerta": 14.50, "cota_atencao": 10.15,
        "cota_emergencia": 17.40, "cota_maxima": 17.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Santarém": {
        "codigo": "16015000", "codigo_ana": "16015000",
        "lat": -2.44, "lon": -54.70, "rio": "Rio Amazonas",
        "cota_atual_ref": 7.80, "cota_max_hist": 10.50, "cota_min_hist": -1.80,
        "cota_media": 5.50, "cota_alerta": 8.50, "cota_atencao": 5.95,
        "cota_emergencia": 10.20, "cota_maxima": 10.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Coari": {
        "codigo": "13650001", "codigo_ana": "13650001",
        "lat": -4.09, "lon": -63.14, "rio": "Rio Solimões",
        "cota_atual_ref": 11.00, "cota_max_hist": 16.20, "cota_min_hist": 1.20,
        "cota_media": 9.50, "cota_alerta": 14.00, "cota_atencao": 9.80,
        "cota_emergencia": 16.00, "cota_maxima": 16.20,
        "sace_bacia": None, "sace_pm": None,
    },

    "Barcelos": {
        "codigo": "14870000", "codigo_ana": "14870000",
        "lat": -0.98, "lon": -62.93, "rio": "Rio Negro",
        "cota_atual_ref": 10.50, "cota_max_hist": 15.50, "cota_min_hist": 1.80,
        "cota_media": 9.00, "cota_alerta": 13.50, "cota_atencao": 9.50,
        "cota_emergencia": 15.20, "cota_maxima": 15.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "São Gabriel da Cachoeira": {
        "codigo": "14960000", "codigo_ana": "14960000",
        "lat": 0.13, "lon": -67.09, "rio": "Rio Negro",
        "cota_atual_ref": 8.00, "cota_max_hist": 12.50, "cota_min_hist": 1.00,
        "cota_media": 6.50, "cota_alerta": 11.00, "cota_atencao": 7.00,
        "cota_emergencia": 12.20, "cota_maxima": 12.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Careiro da Várzea": {
        "codigo": "14100000", "codigo_ana": "14100000",
        "lat": -3.74, "lon": -60.38, "rio": "Rio Amazonas",
        "cota_atual_ref": 24.00, "cota_max_hist": 29.50, "cota_min_hist": 13.00,
        "cota_media": 22.00, "cota_alerta": 28.50, "cota_atencao": 20.00,
        "cota_emergencia": 29.00, "cota_maxima": 29.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Iranduba": {
        "codigo": "13900000", "codigo_ana": "13900000",
        "lat": -3.28, "lon": -60.19, "rio": "Rio Solimões",
        "cota_atual_ref": 17.50, "cota_max_hist": 22.80, "cota_min_hist": 3.50,
        "cota_media": 14.50, "cota_alerta": 20.50, "cota_atencao": 14.00,
        "cota_emergencia": 22.50, "cota_maxima": 22.80,
        "sace_bacia": None, "sace_pm": None,
    },

    "Lábrea": {
        "codigo": "13340000", "codigo_ana": "13340000",
        "lat": -7.26, "lon": -64.80, "rio": "Rio Purus",
        "cota_atual_ref": 9.00, "cota_max_hist": 14.50, "cota_min_hist": 0.80,
        "cota_media": 7.50, "cota_alerta": 12.50, "cota_atencao": 8.50,
        "cota_emergencia": 14.20, "cota_maxima": 14.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Humaitá": {
        "codigo": "13770000", "codigo_ana": "13770000",
        "lat": -7.51, "lon": -63.02, "rio": "Rio Madeira",
        "cota_atual_ref": 8.50, "cota_max_hist": 13.50, "cota_min_hist": 0.50,
        "cota_media": 7.00, "cota_alerta": 11.50, "cota_atencao": 7.80,
        "cota_emergencia": 13.20, "cota_maxima": 13.50,
        "sace_bacia": None, "sace_pm": None,
    },

    "Manicoré": {
        "codigo": "14180000", "codigo_ana": "14180000",
        "lat": -5.81, "lon": -61.30, "rio": "Rio Madeira",
        "cota_atual_ref": 9.50, "cota_max_hist": 15.00, "cota_min_hist": 0.60,
        "cota_media": 8.00, "cota_alerta": 13.00, "cota_atencao": 8.80,
        "cota_emergencia": 14.70, "cota_maxima": 15.00,
        "sace_bacia": None, "sace_pm": None,
    },

    "Borba": {
        "codigo": "14390000", "codigo_ana": "14390000",
        "lat": -4.39, "lon": -59.60, "rio": "Rio Madeira",
        "cota_atual_ref": 10.00, "cota_max_hist": 16.00, "cota_min_hist": 0.80,
        "cota_media": 8.50, "cota_alerta": 14.00, "cota_atencao": 9.50,
        "cota_emergencia": 15.70, "cota_maxima": 16.00,
        "sace_bacia": None, "sace_pm": None,
    },

    "Novo Airão": {
        "codigo": "14940000", "codigo_ana": "14940000",
        "lat": -2.63, "lon": -60.94, "rio": "Rio Negro",
        "cota_atual_ref": 17.00, "cota_max_hist": 22.00, "cota_min_hist": 3.50,
        "cota_media": 13.50, "cota_alerta": 20.00, "cota_atencao": 13.00,
        "cota_emergencia": 21.80, "cota_maxima": 22.00,
        "sace_bacia": None, "sace_pm": None,
    },

    "Maués": {
        "codigo": "14440000", "codigo_ana": "14440000",
        "lat": -3.38, "lon": -57.72, "rio": "Rio Maués-Açu",
        "cota_atual_ref": 5.50, "cota_max_hist": 10.80, "cota_min_hist": -0.50,
        "cota_media": 5.00, "cota_alerta": 9.00, "cota_atencao": 5.50,
        "cota_emergencia": 10.50, "cota_maxima": 10.80,
        "sace_bacia": None, "sace_pm": None,
    },
}

# ── Mapeamento nome → código ANA ──────────────────────────────────────────────
ANA_CODIGOS = {nome: cfg["codigo"] for nome, cfg in ESTACOES.items()}
# Aliases sem acento
ANA_CODIGOS["Obidos"]                    = "17050001"
ANA_CODIGOS["Tefe"]                      = "13760000"
ANA_CODIGOS["Santarem"]                  = "16015000"
ANA_CODIGOS["Sao Gabriel da Cachoeira"]  = "14960000"
ANA_CODIGOS["Labrea"]                    = "13340000"
ANA_CODIGOS["Humaita"]                   = "13770000"
ANA_CODIGOS["Manicore"]                  = "14180000"
ANA_CODIGOS["Novo Airao"]                = "14940000"
ANA_CODIGOS["Maues"]                     = "14440000"

# ── NÍVEIS DE ALERTA ──────────────────────────────────────────────────────────
NIVEIS_ALERTA = {
    "normal":     (0,    0.70),
    "atencao":    (0.70, 1.00),
    "alerta":     (1.00, 1.20),
    "emergencia": (1.20, 999),
}

# ── CAMINHOS ──────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).resolve().parent.parent
CAMINHO_FALLBACK = BASE_DIR / "data" / "fallback.json"
CAMINHO_FALLBACK.parent.mkdir(parents=True, exist_ok=True)

DEBUG = os.getenv("DEBUG", "true").lower() == "true"
