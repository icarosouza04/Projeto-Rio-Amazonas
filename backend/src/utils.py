from datetime import datetime, timedelta
import pandas as pd

def gerar_datas(dias=60):
    """Gera lista de datas dos últimos N dias"""
    hoje = datetime.today()
    return [hoje - timedelta(days=i) for i in range(dias)]

def classificar_nivel_alerta(cota, cota_alerta, cota_maxima):
    """Classifica o nível de alerta baseado na cota"""
    percentual = (cota / cota_alerta) * 100
    
    if percentual < 70:
        return "normal"
    elif percentual < 100:
        return "atencao"
    elif percentual < 120:
        return "alerta"
    else:
        return "emergencia"

def filtrar_dados_recentes(df, dias=7):
    """Filtra apenas os últimos N dias de dados"""
    if 'data' in df.columns:
        df['data'] = pd.to_datetime(df['data'])
        data_limite = datetime.today() - timedelta(days=dias)
        return df[df['data'] >= data_limite]
    return df