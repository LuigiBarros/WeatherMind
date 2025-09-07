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
            # Lê a planilha usando a linha 3 (header=3) como nomes das colunas meteorológicas
            df = pd.read_excel(path, header=3)
            # Remove linhas totalmente vazias
            df = df.dropna(how='all')
            # Remove colunas com todos os valores nulos
            df = df.dropna(axis=1, how='all')
            # Remove acentos e padroniza nomes de colunas para minúsculo
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            # Cria coluna binária 'chuva' a partir de 'precipitation (mm)' (apenas para linhas numéricas)
            if 'precipitation (mm)' in df.columns:
                # Remove linhas onde precipitation (mm) não é número
                df = df[pd.to_numeric(df['precipitation (mm)'], errors='coerce').notnull()]
                df['precipitation (mm)'] = df['precipitation (mm)'].astype(float)
                df['chuva'] = (df['precipitation (mm)'] > 0).astype(int)
            # Remove linhas totalmente vazias
            df = df.dropna(how='all')
            # Remove colunas com todos os valores nulos
            df = df.dropna(axis=1, how='all')
            # Remove acentos e padroniza nomes de colunas para minúsculo
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            # Cria coluna binária 'chuva' a partir de 'precipitation (mm)'
            if 'precipitation (mm)' in df.columns:
                df['chuva'] = (df['precipitation (mm)'] > 0).astype(int)
        else:
            df = pd.read_excel(path)
            df = df.dropna()  # remove linhas com valores nulos
            df.columns = [remover_acentos(str(col)).lower() for col in df.columns]
            for col in df.columns:
                if col.replace(' ', '').replace('_', '').startswith('data') and ('hora' in col or 'hr' in col):
                    df = df.rename(columns={col: 'data/hora'})
            if 'data/hora' in df.columns:
                df['data/hora'] = pd.to_datetime(df['data/hora'], errors='coerce')
        dataframes.append(df)

    # Concatena todas as planilhas em um único DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Garante que a coluna data/hora está em datetime
    if 'data/hora' in combined_df.columns:
        combined_df['data/hora'] = pd.to_datetime(combined_df['data/hora'], errors='coerce')
    return combined_df
