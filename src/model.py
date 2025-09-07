
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import joblib

def train_model(X, y):
    """
    Treina um modelo de classificação para prever chuva.
    Salva o modelo treinado em /models.
    Retorna o modelo treinado + conjunto de teste.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    model.fit(X_train, y_train)
    
    # Salva o modelo treinado
    joblib.dump(model, "models/model.pkl")
    
    return model, X_test, y_test
