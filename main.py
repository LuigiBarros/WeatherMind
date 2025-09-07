from src import data_preprocessing, feature_engineering, model, evaluate, predict

def main():
    # 1. Carrega e limpa os dados de múltiplas planilhas
    excel_files = [
        "data/raw/open-meteo-10.65S37.41W187m.xlsx"
    ]
    df = data_preprocessing.load_and_clean(excel_files)

    print("Primeiras linhas da planilha:")
    print(df.head())

    # 2. Feature Engineering
    X, y = feature_engineering.create_features(df)

    # 3. Normalização (igual ao script antigo)
    from sklearn.preprocessing import StandardScaler
    features = X.columns.tolist()
    scaler = StandardScaler()
    X_normalized = X.copy()
    X_normalized[features] = scaler.fit_transform(X[features])
    df_normalized = X_normalized.copy()
    if 'chuva' in df.columns:
        df_normalized['chuva'] = df['chuva']
    print("\nDados normalizados (primeiras linhas):")
    print(df_normalized.head())

    # 4. Distribuição da variável alvo (Chuva)
    print("\nDistribuição da variável Chuva:")
    print(df["chuva"].value_counts())

    import matplotlib.pyplot as plt
    plt.bar(df["chuva"].value_counts().index, df["chuva"].value_counts().values, color=["blue", "green"])
    plt.xticks([0, 1], ["Não Chove", "Chove"])
    plt.xlabel("Classe (Chuva)")
    plt.ylabel("Número de Registros")
    plt.title("Distribuição da Variável Chuva")
    plt.show()

    # 5. Treinamento do modelo
    trained_model, X_test, y_test = model.train_model(X, y)

    # 6. Avaliação
    evaluate.evaluate_model(trained_model, X_test, y_test)

    # 7. Predição com novos dados (exemplo)
    new_data = {"temperatura": 20, "umidade": 90, "pressao": 1012}  # ajuste nomes conforme colunas
    result = predict.make_prediction(trained_model, new_data)
    print(f"\n📌 Previsão para novos dados: {result}")

if __name__ == "__main__":
    main()
