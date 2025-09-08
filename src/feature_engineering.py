import pandas as pd

def create_features(df):
    colunas_relevantes = [
        'temperature_2m (°c)',
        'relative_humidity_2m (%)',
        'pressure_msl (hpa)',
        'surface_pressure (hpa)'
    ]
    X = df[[col for col in colunas_relevantes if col in df.columns]].copy()
    y = df["chuva"] if "chuva" in df.columns else None
    dados = pd.concat([X, y], axis=1).dropna()
    X = dados[colunas_relevantes]
    y = dados["chuva"]
    return X, y
