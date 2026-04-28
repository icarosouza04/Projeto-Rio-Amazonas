from datetime import datetime
from pathlib import Path

# ── CONFIGURAÇÕES GERAIS ──────────────────────────────────────────────────────
TIMEOUT      = 30
HOJE         = datetime.today()
DIAS_ANALISE = 60
VAZAO_MINIMA = 0

# ── API OPEN-METEO (fallback de tendência) ────────────────────────────────────
OPEN_METEO_URL    = "https://api.open-meteo.com/v1/forecast"
FLOOD_URL         = "https://flood-api.open-meteo.com/v1/flood"
OPEN_METEO_PARAMS = {
    "daily":    "river_discharge",
    "timezone": "America/Manaus"
}

# ── API SACE/SGB ──────────────────────────────────────────────────────────────
# URL padrão: https://www.sgb.gov.br/sace/sace_nivel/api/dados/{bacia}_{pm}_cota.csv
# Dados reais a cada 15 minutos | indice em centímetros → dividir por 100 = metros
SACE_BASE_URL = "https://www.sgb.gov.br/sace/sace_nivel/api/dados"

# ── ESTAÇÕES FLUVIOMÉTRICAS ───────────────────────────────────────────────────
ESTACOES = {
    "Manaus": {
        "codigo":         "14990000",
        "lat":            -3.10,
        "lon":            -60.02,
        "rio":            "Rio Negro",
        "cota_atual_ref": 26.56,
        "cota_max_hist":  29.97,
        "cota_min_hist":  12.11,
        "cota_media":     22.50,
        "cota_alerta":    29.00,
        "cota_atencao":   20.30,
        "cota_emergencia":34.80,
        "cota_maxima":    29.97,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=8 → URL: amazonas_8_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    8,
    },

    "Itacoatiara": {
        "codigo":         "14280000",
        "lat":            -3.14,
        "lon":            -58.44,
        "rio":            "Rio Amazonas",
        "cota_atual_ref": 13.00,
        "cota_max_hist":  16.83,
        "cota_min_hist":   1.20,
        "cota_media":      9.50,
        "cota_alerta":    14.00,
        "cota_atencao":    9.80,
        "cota_emergencia": 16.80,
        "cota_maxima":    16.83,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=26 → URL: amazonas_26_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    26,
    },

    "Manacapuru": {
        "codigo":         "13850000",
        "lat":            -3.31,
        "lon":            -60.61,
        "rio":            "Rio Solimões",
        "cota_atual_ref": 18.00,
        "cota_max_hist":  23.50,
        "cota_min_hist":   3.20,
        "cota_media":     15.00,
        "cota_alerta":    21.00,
        "cota_atencao":   14.70,
        "cota_emergencia":25.20,
        "cota_maxima":    23.50,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=12 → URL: amazonas_12_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    12,
    },

    "Parintins": {
        "codigo":         "14540000",
        "lat":            -2.63,
        "lon":            -56.74,
        "rio":            "Rio Amazonas",
        "cota_atual_ref": 10.50,
        "cota_max_hist":  13.80,
        "cota_min_hist":  -1.76,
        "cota_media":      7.20,
        "cota_alerta":    11.50,
        "cota_atencao":    8.05,
        "cota_emergencia": 13.80,
        "cota_maxima":    13.80,
        "rc_a": None,
        "rc_b": None,
        # Parintins não apareceu no HTML do SACE — usa Open-Meteo como fallback
        "sace_bacia": None,
        "sace_pm":    None,
    },

    "Óbidos": {
        "codigo":         "17050001",
        "lat":            -1.92,
        "lon":            -55.52,
        "rio":            "Rio Amazonas",
        "cota_atual_ref":  8.50,
        "cota_max_hist":  11.20,
        "cota_min_hist":  -2.53,
        "cota_media":      5.80,
        "cota_alerta":     9.00,
        "cota_atencao":    6.30,
        "cota_emergencia": 10.80,
        "cota_maxima":    11.20,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=34 → URL: amazonas_34_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    34,
    },

    "Tefé": {
        "codigo":         "13760000",
        "lat":            -3.37,
        "lon":            -64.72,
        "rio":            "Rio Solimões",
        "cota_atual_ref": 12.00,
        "cota_max_hist":  17.50,
        "cota_min_hist":   1.46,
        "cota_media":     10.20,
        "cota_alerta":    14.50,
        "cota_atencao":   10.15,
        "cota_emergencia": 17.40,
        "cota_maxima":    17.50,
        "rc_a": None,
        "rc_b": None,
        # Tefé não apareceu no HTML — usa Open-Meteo como fallback
        "sace_bacia": None,
        "sace_pm":    None,
    },

    "Santarém": {
        "codigo":         "16015000",
        "lat":            -2.44,
        "lon":            -54.70,
        "rio":            "Rio Amazonas",
        "cota_atual_ref":  7.80,
        "cota_max_hist":  10.50,
        "cota_min_hist":  -1.80,
        "cota_media":      5.50,
        "cota_alerta":     8.50,
        "cota_atencao":    5.95,
        "cota_emergencia": 10.20,
        "cota_maxima":    10.50,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=37 → URL: amazonas_37_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    37,
    },

    "Tabatinga": {
        "codigo":         "13020000",
        "lat":            -4.25,
        "lon":            -69.94,
        "rio":            "Rio Solimões",
        "cota_atual_ref": 11.10,
        "cota_max_hist":  13.50,
        "cota_min_hist":  -2.34,
        "cota_media":      7.50,
        "cota_alerta":    11.00,
        "cota_atencao":    7.70,
        "cota_emergencia": 13.20,
        "cota_maxima":    13.50,
        "rc_a": None,
        "rc_b": None,
        # SACE: pm=15 → URL: amazonas_15_cota.csv
        "sace_bacia": "amazonas",
        "sace_pm":    15,
    },
}

# ── NÍVEIS DE ALERTA ──────────────────────────────────────────────────────────
NIVEIS_ALERTA = {
    "normal":     (0,    0.70),
    "atencao":    (0.70, 1.00),
    "alerta":     (1.00, 1.20),
    "emergencia": (1.20, 999),
}

# ── CAMINHOS ─────────────────────────────────────────────────────────────────
CAMINHO_FALLBACK = Path(__file__).resolve().parent.parent / 'data' / 'fallback.json'

DEBUG = True
