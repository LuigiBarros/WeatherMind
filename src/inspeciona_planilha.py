import pandas as pd

file_path = "data/raw/open-meteo-10.65S37.41W187m.xlsx"

df = pd.read_excel(file_path)
print("Colunas da planilha:")
print(df.columns)
print("Primeiras linhas:")
print(df.head())
