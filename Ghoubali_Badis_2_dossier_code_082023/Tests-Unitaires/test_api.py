import pytest
from unittest.mock import patch, Mock

# Cas de test pour le chargement du modèle
def test_model_loading():
    import joblib
    import os
    # Détermine le chemin du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du modèle
    model_path = os.path.join(current_directory, "..", "Simulations", "Best_model", "model.pkl")
    # Charge le modèle
    model = joblib.load(model_path)
    # Assure que le modèle est bien chargé
    assert model is not None, "Le modèle n'a pas été correctement chargé."

# Cas de test pour le chargement du CSV
def test_csv_loading():
    import pandas as pd
    import os
    # Détermine le chemin du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du fichier CSV
    csv_path = os.path.join(current_directory, "..", "Simulations", "df_test.csv")
    # Charge le CSV dans un DataFrame
    df = pd.read_csv(csv_path)
    # Assure que le DataFrame n'est pas vide
    assert not df.empty, "Le DataFrame est vide, le CSV n'a pas été chargé correctement."

# Cas de test pour la prédiction
def test_prediction():
    import joblib
    import os
    import pandas as pd
    # Détermine le chemin du répertoire courant
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Détermine le chemin du modèle et du fichier CSV
    model_path = os.path.join(current_directory, "..", "Simulations", "Best_model", "model.pkl")
    csv_path = os.path.join(current_directory, "..", "Simulations", "df_test.csv")
    # Charge le modèle et le fichier CSV
    model = joblib.load(model_path)
    df = pd.read_csv(csv_path)
    # Prend un échantillon pour la prédiction
    sample = df.iloc[0].drop(labels=["SK_ID_CURR"])
    prediction = model.predict_proba([sample])
    # Assure que la prédiction est effectuée
    assert prediction is not None, "La prédiction a échoué."

