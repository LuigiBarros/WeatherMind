import pandas as pd

# Caminho para a nova planilha
file_path = "data/raw/open-meteo-10.65S37.41W187m.xlsx"

# Lê apenas as primeiras linhas para inspecionar as colunas
df = pd.read_excel(file_path)
print("Colunas da planilha:")
print(df.columns)
print("Primeiras linhas:")
print(df.head())
