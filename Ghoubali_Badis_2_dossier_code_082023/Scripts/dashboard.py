import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(layout='wide') 

def compute_color(value):
    if 0 <= value < 48:
        return "green"  
    elif 48 <= value <= 100:
        return "red" 


def format_value(val):
    if pd.isna(val):
        return val
    if isinstance(val, (float, int)):
        if val == int(val):
            return int(val)
        return round(val, 2)
    return val


st.markdown("<h1 style='text-align: center; color: black;'>Estimation du risque de non-remboursement</h1>", unsafe_allow_html=True)
sk_id_curr = st.text_input("Entrez le SK_ID_CURR:")
col1, col2 = st.columns([1, 20])

if col1.button('Run'):
    response = requests.post("http://localhost:5000/predict", json={'SK_ID_CURR': int(sk_id_curr)})
    if response.status_code != 200:
        st.error(f"Erreur lors de l'appel à l'API: {response.status_code}")
        st.stop()
    
    data = response.json()
    proba = data['probability']
    feature_names = data['feature_names']
    shap_values = data['shap_values']
    feature_values = data['feature_values']
    shap_values = [val[0] if isinstance(val, list) else val for val in shap_values]
    shap_df = pd.DataFrame(list(zip(feature_names, shap_values, [format_value(val) for val in feature_values])), columns=['Feature', 'SHAP Value', 'Feature Value'])

    color = compute_color(proba)
    col2.markdown(f"La probabilité que ce client ne puisse pas rembourser son crédit est de <span style='color:{color}; font-weight:bold;'>{proba:.2f}%</span> (tolérance max: <strong>48%</strong>)", unsafe_allow_html=True)

    decision_message = "Le prêt sera accordé." if proba < 48 else "Le prêt ne sera pas accordé."
    st.markdown(f"<div style='text-align: center; color:{color}; font-size:30px; border:2px solid {color}; padding:10px;'>{decision_message}</div>", unsafe_allow_html=True)


    # Top 10 des fonctionnalités augmentant la probabilité
    top_positive_shap = shap_df.sort_values(by='SHAP Value', ascending=False).head(10)
    fig_positive = go.Figure(data=[
        go.Bar(y=top_positive_shap['Feature'], x=top_positive_shap['SHAP Value'], orientation='h')
    ])
    
    annotations = []
    for y_val, x_val, feat_val in zip(top_positive_shap['Feature'], top_positive_shap['SHAP Value'], top_positive_shap['Feature Value']):
        if pd.isna(feat_val):
            formatted_feat_val = feat_val
        else:
            formatted_feat_val = int(feat_val) if feat_val == int(feat_val) else feat_val
        annotations.append(dict(x=x_val, y=y_val, text=f'<b>{formatted_feat_val}</b>', showarrow=False, xanchor='right', yanchor='middle', font=dict(color='white')))



    fig_positive.update_layout(annotations=annotations)

    fig_positive.update_layout(
        title_text="Top 10 des fonctionnalités augmentant le risque de non-remboursement",
        title_x=0.25,
        title_y=0.88,
        title_font=dict(size=16),  # Réduire la taille de la police du titre
        yaxis=dict(
            categoryorder='total ascending', 
            tickfont=dict(size=14)  # Augmenter la taille de la police pour les annotations
        ),
        height=600
    )
    fig_positive.update_xaxes(title_text="Impact des fonctionnalités")  # Ajout de l'annotation à l'axe des x

    # Top 10 des fonctionnalités réduisant la probabilité
    top_negative_shap = shap_df.sort_values(by='SHAP Value').head(10)
    fig_negative = go.Figure(data=[
        go.Bar(y=top_negative_shap['Feature'], x=top_negative_shap['SHAP Value'], orientation='h')
    ])

    # Générer des annotations pour top_negative_shap
    annotations_negative = []
    for y_val, x_val, feat_val in zip(top_negative_shap['Feature'], top_negative_shap['SHAP Value'], top_negative_shap['Feature Value']):
        if pd.isna(feat_val):
            formatted_feat_val = feat_val
        else:
            formatted_feat_val = int(feat_val) if feat_val == int(feat_val) else feat_val
        annotations_negative.append(dict(x=x_val, y=y_val, text=f'<b>{formatted_feat_val}</b>', showarrow=False, xanchor='left', yanchor='middle', font=dict(color='white')))


    # Mettre à jour le graphique fig_negative pour inclure ces annotations
    fig_negative.update_layout(annotations=annotations_negative)

    fig_negative.update_layout(
        title_text="Top 10 des fonctionnalités réduisant le risque de non-remboursement",
        title_x=0.25,
        title_y=0.88,
        title_font=dict(size=16),  
        yaxis=dict(
            categoryorder='total descending',
            side='right',
            tickfont=dict(size=14)  
        ),
        height=600
    )
    fig_negative.update_xaxes(title_text="Impact des fonctionnalités") 

    # Créer une nouvelle ligne pour les graphiques
    col_chart1, col_chart2 = st.columns(2)
    col_chart1.plotly_chart(fig_positive)
    col_chart2.plotly_chart(fig_negative)


