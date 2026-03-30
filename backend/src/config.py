from datetime import datetime
from pathlib import Path


# CONFIGURAÇÕES GERAIS


TIMEOUT = 30  # Tempo máximo de requisição (segundos)
HOJE = datetime.today()

# Quantidade de dias analisados
DIAS_ANALISE = 60

# Vazão mínima considerada (filtro)
VAZAO_MINIMA = 50000


# CONFIGURAÇÃO DA API


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Parâmetros padrão da API
OPEN_METEO_PARAMS = {
    "daily": "river_discharge",
    "timezone": "America/Manaus"
}


# ESTAÇÕES FLUVIOMÉTRICAS


ESTACOES = {
    "Manaus": {
        "codigo": "14100000",
        "lat": -3.10,
        "lon": -60.02,
        "cota_maxima": 39.5,
        "cota_alerta": 29.0,
        "rc_a": 0.000312,
        "rc_b": 0.652
    },

    "Itacoatiara": {
        "codigo": "14280000",
        "lat": -3.14,
        "lon": -58.44,
        "cota_maxima": 44.0,
        "cota_alerta": 35.0,
        "rc_a": 0.000285,
        "rc_b": 0.641
    },

    "Parintins": {
        "codigo": "14540000",
        "lat": -2.63,
        "lon": -56.74,
        "cota_maxima": 47.0,
        "cota_alerta": 42.0,
        "rc_a": 0.000270,
        "rc_b": 0.638
    },

    "Óbidos": {
        "codigo": "17050001",
        "lat": -1.92,
        "lon": -55.52,
        "cota_maxima": 20.0,
        "cota_alerta": 15.0,
        "rc_a": 0.000055,
        "rc_b": 0.590
    },

    "Tefé": {
        "codigo": "13760000",
        "lat": -3.37,
        "lon": -64.72,
        "cota_maxima": 35.0,
        "cota_alerta": 28.0,
        "rc_a": 0.000220,
        "rc_b": 0.621
    },

    "Santarém": {
        "codigo": "16015000",
        "lat": -2.44,
        "lon": -54.7,
        "cota_maxima": 32.0,
        "cota_alerta": 26.0,
        "rc_a": 0.000240,
        "rc_b": 0.634
    },

    "Tabatinga": {
        "codigo": "13020000",
        "lat": -4.25,
        "lon": -69.94,
        "cota_maxima": 15.0,
        "cota_alerta": 11.0,
        "rc_a": 0.000180,
        "rc_b": 0.605
    }
}

CAMINHO_FALLBACK = Path(__file__).resolve().parent.parent / 'data' / 'fallback.json'


# CONFIGURAÇÃO DE ALERTAS


NIVEIS_ALERTA = {
    "normal": (0, 0.7),       # até 70% da cota de alerta
    "atencao": (0.7, 1.0),    # entre 70% e 100%
    "alerta": (1.0, 1.2),     # acima da cota de alerta
    "emergencia": (1.2, 999)  # muito acima
}


# CAMINHOS DE ARQUIVO






# MODO DEBUG


DEBUG = True