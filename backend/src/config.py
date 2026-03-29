from datetime import datetime


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

        # Limites
        "cota_maxima": 39.5,
        "cota_alerta": 29.0,

        # Curva-chave (vazão → cota)
        "rc_a": 0.000312,
        "rc_b": 0.652
    },

    "Óbidos": {
        "codigo": "17050001",
        "lat": -1.92,
        "lon": -55.52,

        "cota_maxima": 8.0,
        "cota_alerta": 6.0,

        "rc_a": 0.000210,
        "rc_b": 0.690
    },

    "Itacoatiara": {
        "codigo": "16030000",
        "lat": -3.14,
        "lon": -58.44,

        "cota_maxima": 14.0,
        "cota_alerta": 11.0,

        "rc_a": 0.000280,
        "rc_b": 0.670
    },

    "Parintins": {
        "codigo": "16350002",
        "lat": -2.63,
        "lon": -56.73,

        "cota_maxima": 9.5,
        "cota_alerta": 7.0,

        "rc_a": 0.000250,
        "rc_b": 0.680
    }
}


# CONFIGURAÇÃO DE ALERTAS


NIVEIS_ALERTA = {
    "normal": (0, 0.7),       # até 70% da cota de alerta
    "atencao": (0.7, 1.0),    # entre 70% e 100%
    "alerta": (1.0, 1.2),     # acima da cota de alerta
    "emergencia": (1.2, 999)  # muito acima
}


# CAMINHOS DE ARQUIVO


CAMINHO_FALLBACK = "data/fallback.json"



# MODO DEBUG


DEBUG = True