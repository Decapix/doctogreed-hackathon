import streamlit as st
import pandas as pd
import requests
import json
import logging

# username = st.secrets["username"]
username = "felou"
# password = st.secrets["password"]

def home_page():
    st.title("Bienvenue sur notre plateforme médicale")
    st.header("Votre historique médical")

    # Exemple d'historique médical (à remplacer par des données réelles)
    historique = [
        {"date": "2023-01-01", "description": "Consultation pour douleur thoracique"},
        {"date": "2023-05-15", "description": "Suivi post-opératoire"},
    ]

    for entry in historique:
        st.write(f"**{entry['date']}**: {entry['description']}")

def post_consultation_page():
    st.write("Bienvenue sur votre espace personnel. Ici, vous pouvez consulter vos rapports médicaux.")

    st.header("📂 Vos documents médicaux")
    sample_reports = ["rapport_Alice.pdf"]

    for report in sample_reports:
        with open(report, "rb") as file:
            st.download_button(label=f"📥 Télécharger {report}", data=file, file_name=report, mime="application/pdf", key="download_btn", use_container_width=True)

    st.title("Post-consultation")

    st.header("Votre ordonnance")
    st.write("Médicament : Aspirine")
    st.write("Dosage : 500mg")
    st.write("Fréquence : 2 fois par jour")

    st.header("Explications de prise de traitement")
    st.write("Prenez le médicament avec un verre d'eau.")

def load_questions(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def save_responses(file_path, responses):
    with open(file_path, 'w') as file:
        json.dump(responses, file, indent=4)

def fetch_questions():
    try:
        response = requests.get("http://backend:8000/diagnostic")
        response.raise_for_status()  # Vérifie les erreurs HTTP
        questions = response.json()
        return questions
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des questions: {e}")
        return []
    except ValueError as e:
        st.error(f"Erreur de décodage JSON: {e}")
        st.write("Réponse brute de l'API:")
        st.write(response.text)  # Affiche la réponse brute pour le débogage
        return []
    
def chatbot_page():
    st.title("📋 Questionnaire Médical")
    st.caption("Répondez aux questions suivantes pour aider votre médecin à mieux comprendre votre situation.")

    # questions = fetch_questions()
    questions = [
    {"id": 1, "text": "Avez-vous des douleurs thoraciques ?", "response_type": "boolean"},
    {"id": 2, "text": "Sur une échelle de 1 à 5, comment évalueriez-vous votre niveau de douleur ?", "response_type": "scale", "range": {1: "Pas du tout", 2: "Un peu", 3: "Modéré", 4: "Beaucoup", 5: "Énormément"}},
    {"id": 3, "text": "À quel point êtes-vous satisfait de votre traitement actuel ?", "response_type": "scale", "range": {1: "Pas satisfait", 2: "Peu satisfait", 3: "Neutre", 4: "Satisfait", 5: "Très satisfait"}}
]

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "responses" not in st.session_state:
        st.session_state.responses = []

    patient_name = st.text_input("Nom du patient", key="patient_name")
    patient_gender = st.selectbox("Genre du patient", ["","Homme", "Femme", "Autre"], key="patient_gender")
    patient_gender_id = 1 if patient_gender == "Homme" else 2 if patient_gender == "Femme" else 3 if patient_gender == "Autre" else None
    # Afficher l'historique des réponses
    for i, (question, response) in enumerate(zip(questions, st.session_state.responses)):
        st.write(f"**Question {i+1}**: {question['text']}")
        st.write(f"**Réponse**: {response}")

    # Poser la question actuelle
    if st.session_state.current_question_index < len(questions):
        current_question = questions[st.session_state.current_question_index]
        st.write(f"**Question {st.session_state.current_question_index + 1}**: {current_question['text']}")
        response_key = f"question_{st.session_state.current_question_index}"
        if current_question["response_type"] == "boolean":
            user_response = st.radio("Votre réponse", ["Oui", "Non"], key=response_key)
            response = 0 if user_response == "Non" else 1
        elif current_question["response_type"] == "scale":
            # Affichage de l'échelle avec labels
            range_values = list(current_question["range"].keys())
            response = st.select_slider("Votre réponse", options=range_values, 
                                        format_func=lambda x: current_question["range"][x], key=response_key)
        
        if st.button("Continuer"):
            if response is not None:
                st.session_state.responses.append(response)
                st.session_state.current_question_index += 1
                st.query_params = {"page": "questionnaire", "index": st.session_state.current_question_index}
                st.rerun()

    # Cas 2 : Toutes les questions ont été répondues
    else:
        # Vérifier que les informations patient sont bien renseignées
        if patient_name == "":
            st.warning("Veuillez entrer un nom pour continuer.")
        elif patient_gender == "":
            st.warning("Veuillez sélectionner un genre pour continuer.")
        else:
            # Construction de la structure des réponses
            # Ici, pour chaque question, si elle possède un "range", on récupère les valeurs min, max et le label associé
            structured_responses = {
                "patient_name": patient_name,
                "patient_gender": patient_gender_id,
                "responses": {
                    question["id"]: [
                        response,
                        min(question["range"].keys()) if "range" in question else None,
                        max(question["range"].keys()) if "range" in question else None,
                        question["range"].get(response) if "range" in question else None,
                        question["text"]
                    ]
                    for question, response in zip(questions, st.session_state.responses)
                }
            }
            save_responses('responses.json', structured_responses)
            st.write("Merci d'avoir répondu à toutes les questions. Vos réponses ont été transférées à un médecin.")

            # Envoi des données vers le backend
            with open('responses.json', 'r') as file:
                data = json.load(file)
            for key, value_list in data["responses"].items():
                # On remplace None par "-1" si besoin, puis on jointe les éléments avec une virgule
                data["responses"][key] = ", ".join(
                    [str(item) if item is not None else "-1" for item in value_list]
                )
            
            logging.info(f"Données envoyées à l'API: {data}")
            url = "http://backend:8000/recup-diagnostic/"
            response_api = requests.post(url, json=data)
            # Vérifier la réponse de l'API
            if response_api.status_code == 200:
                logging.info("Diagnostic enregistré avec succès.")
            else:
                logging.error(f"Erreur lors de l'enregistrement du diagnostic: {response_api.status_code}")
                logging.error(f"Réponse de l'API: {response_api.text}")

def generate_pdf():
    # Fonction pour générer un PDF (exemple basique)
    pdf_content = "Voici votre rapport médical"
    return pdf_content

def send_pdf(pdf_content):
    # Fonction pour envoyer le PDF (ici simulée)
    st.write("PDF généré et envoyé avec succès.")

def main():
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Accueil"):
        st.session_state.page = "home"
    if st.sidebar.button("Post-consultation"):
        st.session_state.page = "post_consultation"
    if st.sidebar.button("Chatbot"):
        st.session_state.page = "chatbot"

    if 'page' not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "post_consultation":
        post_consultation_page()
    elif st.session_state.page == "chatbot":
        chatbot_page()
        
    # Boutons pour générer et envoyer le PDF
    pdf_content = generate_pdf()
    
    if st.button("Générer et envoyer le PDF", key="generate_pdf", help="Générer un rapport médical en PDF", use_container_width=True):
        send_pdf(pdf_content)

if __name__ == "__main__":
    main()
