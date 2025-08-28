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
        df = pd.read_excel(path)
        df = df.dropna()  # remove linhas com valores nulos
        # Remove acentos e padroniza nomes de colunas para minúsculo
        df.columns = [remover_acentos(col).lower() for col in df.columns]
        # Renomeia possíveis variações de data/hora para 'data/hora'
        for col in df.columns:
            if col.replace(' ', '').replace('_', '').startswith('data') and ('hora' in col or 'hr' in col):
                df = df.rename(columns={col: 'data/hora'})
        # Converte coluna de data/hora para datetime, se existir
        if 'data/hora' in df.columns:
            df['data/hora'] = pd.to_datetime(df['data/hora'], errors='coerce')
        dataframes.append(df)

    # Concatena todas as planilhas em um único DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Garante que a coluna data/hora está em datetime
    if 'data/hora' in combined_df.columns:
        combined_df['data/hora'] = pd.to_datetime(combined_df['data/hora'], errors='coerce')
    return combined_df
