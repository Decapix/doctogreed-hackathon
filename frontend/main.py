import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Bienvenue", page_icon="🏥", layout="wide")

# Style CSS pour le fond bleu
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to bottom, rgb(37, 150, 190), #0066FF); /* Gradient entre les deux couleurs */
            color: white;
            text-align: center;
        }
        h1 {
            font-size: 3em;
            font-weight: bold;
        }
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre centré
st.markdown("<h1>🏥 Bienvenue sur Care Pulse</h1>", unsafe_allow_html=True)

# Utilisation de st.columns pour centrer l'image et le texte
col1, col2, col3 = st.columns([1, 2, 1])  # Ajuste la largeur des colonnes

with col2:
    st.image("./care_pulse.png", use_container_width=False, caption="Care Pulse", width=420)  # Image centrée dans la colonne du milieu
    st.write("Nous vous souhaitons la bienvenue sur notre plateforme !")
