import pandas as pd
import joblib

def make_prediction(model, new_data: dict):
    """
    Recebe um dicionário com dados do clima e retorna previsão.
    Exemplo:
    new_data = {"temperatura": 20, "umidade": 90, "pressao": 1012}
    """
    import datetime
    # Gera features temporais se não existirem
    df = pd.DataFrame([new_data])
    # Adiciona colunas de features temporais se o modelo espera
    for col in ['Ano', 'Mes', 'Dia', 'Hora', 'Minuto']:
        if col not in df.columns:
            df[col] = datetime.datetime.now().__getattribute__(col.lower()) if hasattr(datetime.datetime.now(), col.lower()) else 0
    # Garante ordem das colunas igual ao modelo
    if hasattr(model, 'feature_names_in_'):
        df = df.reindex(columns=model.feature_names_in_, fill_value=0)
    prediction = model.predict(df)[0]
    return "Vai chover ☔" if prediction == 1 else "Não vai chover ☀️"
