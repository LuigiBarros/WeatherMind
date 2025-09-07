import pandas as pd

file_path = "data/raw/open-meteo-10.65S37.41W187m.xlsx"
df = pd.read_excel(file_path, header=3)
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)
print("Colunas:", df.columns.tolist())
print("Primeiras linhas:")
print(df.head(10))
print("Tipos de dados:")
print(df.dtypes)
print("Resumo de valores nulos:")
print(df.isnull().sum())
