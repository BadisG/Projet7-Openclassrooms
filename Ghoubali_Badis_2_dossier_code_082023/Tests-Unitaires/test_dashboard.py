import pytest
from unittest.mock import patch, Mock
import os
import sys

# Obtenez le répertoire de travail actuel
cwd = os.getcwd()

# Créez un chemin relatif vers le dossier contenant dashboard.py
scripts_dir = os.path.join(cwd, "..", "Scripts")

# Ajoutez ce chemin au sys.path pour pouvoir importer des modules à partir de ce dossier
sys.path.append(scripts_dir)

# Simulation d'un état pour st.session_state
mocked_session_state = {'state': {'data_received': False, 'data': None, 'last_sk_id_curr': None}}

# Définir le décorateur pytest pour simuler st.session_state
@pytest.fixture
def mocked_st(monkeypatch):
    monkeypatch.setattr("streamlit.session_state", mocked_session_state)
    return mocked_session_state

# Utilise pytest.mark pour appliquer le mock à des tests spécifiques
@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_compute_color(mocked_st):
    from dashboard import compute_color
    # Teste la fonction compute_color pour différentes valeurs
    assert compute_color(30) == "green", "Erreur dans la fonction compute_color."
    assert compute_color(50) == "red", "Erreur dans la fonction compute_color."

@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_format_value(mocked_st):
    from dashboard import format_value
    # Teste la fonction format_value pour différentes valeurs
    assert format_value(5.67) == 5.67, "Erreur dans la fonction format_value."
    assert format_value(5.00) == 5, "Erreur dans la fonction format_value."

@pytest.mark.parametrize('mocked_st', [mocked_session_state], indirect=True)
def test_find_closest_description(mocked_st):
    from dashboard import find_closest_description, definition_features_df
    # Teste la fonction pour trouver la description la plus proche d'un terme donné
    description = find_closest_description("AMT_INCOME_TOTAL", definition_features_df)
    assert description is not None, "Erreur dans la fonction find_closest_description."

def test_get_state(mocked_st):	
    from dashboard import get_state
    state = get_state()
    assert isinstance(state, dict), "La fonction get_state doit renvoyer un dictionnaire."
    assert "data_received" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'data_received'."
    assert "data" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'data'."
    assert "last_sk_id_curr" in state, "Le dictionnaire renvoyé par get_state doit contenir la clé 'last_sk_id_curr'."
