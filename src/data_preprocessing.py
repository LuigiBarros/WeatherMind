import pandas as pd
from typing import List

def load_and_clean(paths: List[str]):
    """
    Carrega e limpa dados brutos de múltiplos arquivos Excel.
    - paths: lista de caminhos dos arquivos Excel
    - Remove valores nulos
    - Converte tipos de dados
    - Retorna um DataFrame único pronto para feature engineering
    """
    dataframes = []


    import unicodedata
    def remover_acentos(txt):
        return ''.join(c for c in unicodedata.normalize('NFKD', txt) if not unicodedata.combining(c))

    for path in paths:
        if 'open-meteo' in path:
            df = pd.read_excel(path, header=3)
            df = df.dropna(how='all')
            df = df.dropna(axis=1, how='all')
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            if 'precipitation (mm)' in df.columns:
                df = df[pd.to_numeric(df['precipitation (mm)'], errors='coerce').notnull()]
                df['precipitation (mm)'] = df['precipitation (mm)'].astype(float)
                df['chuva'] = (df['precipitation (mm)'] > 0).astype(int)
            df = df.dropna(how='all')
            df = df.dropna(axis=1, how='all')
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            if 'precipitation (mm)' in df.columns:
                df['chuva'] = (df['precipitation (mm)'] > 0).astype(int)
        else:
            df = pd.read_excel(path)
            df = df.dropna()
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            for col in df.columns:
                if col.replace(' ', '').replace('_', '').startswith('data') and ('hora' in col or 'hr' in col):
                    df = df.rename(columns={col: 'data/hora'})
            if 'data/hora' in df.columns:
                df['data/hora'] = pd.to_datetime(df['data/hora'], errors='coerce')
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    if 'data/hora' in combined_df.columns:
        combined_df['data/hora'] = pd.to_datetime(combined_df['data/hora'], errors='coerce')
    return combined_df
