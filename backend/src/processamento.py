import pandas as pd

def vazao_para_cota(df, a, b, cota_maxima):
    """Converte vazão em cota usando curva-chave (rating curve)"""
    df = df.copy()
    df["cota_m"] = a * (df["vazao"] ** b)
    df["cota_m"] = df["cota_m"].clip(upper=cota_maxima)
    return df