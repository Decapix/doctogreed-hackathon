import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Bienvenue", page_icon="🏥", layout="wide")

# Style CSS pour le fond bleu
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0066FF; /* Bleu Doctolib */
            color: white;
            text-align: center;
        }
        h1 {
            font-size: 3em;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre centré
st.markdown("<h1>🏥 Bienvenue sur Care Pulse</h1>", unsafe_allow_html=True)

