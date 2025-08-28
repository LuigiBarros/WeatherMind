import pandas as pd

def create_features(df):
    if 'data/hora' in df.columns:
        df['Ano'] = df['data/hora'].dt.year
        df['Mes'] = df['data/hora'].dt.month
        df['Dia'] = df['data/hora'].dt.day
        df['Hora'] = df['data/hora'].dt.hour
        df['Minuto'] = df['data/hora'].dt.minute
        df = df.drop(columns=['data/hora'])

    X = df.drop(columns=["chuva"])
    # Remove colunas não numéricas (datetime e objeto)
    X = X.select_dtypes(include=["number"])
    y = df["chuva"]
    return X, y
