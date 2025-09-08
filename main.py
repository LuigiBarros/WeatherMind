from src import data_preprocessing, feature_engineering

def main():
    print("Escolha uma opção:")
    print("1 - Treinar e avaliar IA (walk-forward)")
    print("2 - Inserir 3 linhas de dados para previsão manual")
    opcao = input("Digite 1 ou 2: ").strip()

    if opcao == "1":
        excel_files = ["data/raw/open-meteo-10.65S37.41W187m.xlsx"]
        df = data_preprocessing.load_and_clean(excel_files)
        X, y = feature_engineering.create_features(df)
        from sklearn.preprocessing import StandardScaler
        features = X.columns.tolist()
        scaler = StandardScaler()
        X_normalized = X.copy()
        X_normalized[features] = scaler.fit_transform(X[features])
        import matplotlib.pyplot as plt
        plt.bar(df["chuva"].value_counts().index, df["chuva"].value_counts().values, color=["blue", "green"])
        plt.xticks([0, 1], ["Não Chove", "Chove"])
        plt.xlabel("Classe (Chuva)")
        plt.ylabel("Número de Registros")
        plt.title("Distribuição da Variável Chuva")
        plt.show()
        from sklearn.neural_network import MLPClassifier
        from sklearn.metrics import accuracy_score
        y_true = []
        y_pred = []
        window = 3
        for i in range(window, len(X)):
            X_train = X.iloc[i-window:i]
            y_train = y.iloc[i-window:i]
            X_test = X.iloc[[i]]
            y_test = y.iloc[[i]]
            model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
            model.fit(X_train, y_train)
            pred = model.predict(X_test)[0]
            y_true.append(y_test.values[0])
            y_pred.append(pred)
        acc = accuracy_score(y_true, y_pred)
        print(f"\n🎯 Acurácia walk-forward: {acc:.2f}")
        from sklearn.metrics import classification_report, confusion_matrix
        print("\n📊 Relatório de Classificação:")
        print(classification_report(y_true, y_pred))
        import seaborn as sns
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(5,4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Matriz de Confusão (Walk-Forward)")
        plt.xlabel("Previsto")
        plt.ylabel("Real")
        plt.savefig("reports/figures/matriz_confusao.png")
        plt.close()

    elif opcao == "2":
        features = [
            'temperature_2m (°c)',
            'relative_humidity_2m (%)',
            'pressure_msl (hpa)',
            'surface_pressure (hpa)'
        ]
        ultimos = []
        for i in range(3):
            linha = {}
            print(f"\nLinha {i+1}:")
            for feat in features:
                valor = float(input(f"{feat}: "))
                linha[feat] = valor
            ultimos.append(linha)
        import pandas as pd
        excel_files = ["data/raw/open-meteo-10.65S37.41W187m.xlsx"]
        df = data_preprocessing.load_and_clean(excel_files)
        X, y = feature_engineering.create_features(df)
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        from sklearn.neural_network import MLPClassifier
        model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000, random_state=42)
        model.fit(X_scaled, y)
        X_input = pd.DataFrame(ultimos)
        X_input_scaled = scaler.transform(X_input)
        pred = model.predict([X_input_scaled[-1]])[0]
        print("\nPrevisão para a próxima hora:")
        print("Vai chover ☔" if pred == 1 else "Não vai chover ☀️")
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()
