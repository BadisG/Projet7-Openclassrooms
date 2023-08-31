import os

import joblib
import pandas as pd
import shap
from flask import Flask, jsonify, request

app = Flask(__name__)

model = None  # Initialisation à None

# Récupérez le répertoire actuel du fichier api.py
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.route("/predict", methods=['POST'])
def predict():
    data = request.json
    sk_id_curr = data['SK_ID_CURR']

    # Construisez le chemin complet vers df_test.csv en utilisant le chemin relatif depuis l'emplacement de api.py
    csv_path = os.path.join(current_directory, "..", "Simulations", "df_test.csv")
    # Charger le CSV
    df = pd.read_csv(csv_path)
    sample = df[df['SK_ID_CURR'] == sk_id_curr]

    # Supprimer la colonne ID pour la prédiction
    sample = sample.drop(columns=['SK_ID_CURR'])

    # Prédire
    prediction = model.predict_proba(sample)
    proba = prediction[0][1] # Probabilité de la seconde classe

    # Calculer les valeurs SHAP pour l'échantillon donné
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(sample)
    
    # Retourner les valeurs SHAP avec la probabilité
    return jsonify({
        'probability': proba*100, 
        'shap_values': shap_values[1][0].tolist(),
        'feature_names': sample.columns.tolist(),
        'feature_values': sample.values[0].tolist()
    })

# Déplacer la logique de chargement du modèle à l'intérieur de la clause if __name__ == "__main__":
if __name__ == "__main__":
    model_path = os.path.join(current_directory, "..", "Simulations", "Best_model", "model.pkl")
    model = joblib.load(model_path)
    app.run(debug=True)