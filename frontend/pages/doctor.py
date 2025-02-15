import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

def generate_priority_list():
    """Génération de données fictives pour les scores des patients."""
    np.random.seed(42)
    patients = ["Alice", "Bob", "Charlie", "David", "Emma"]
    scores = np.random.uniform(0, 10, len(patients))
    df = pd.DataFrame({"Nom": patients, "Score": scores})
    df = df.sort_values(by="Score", ascending=False)
    return df

def color_code(score):
    """Retourne la couleur en fonction du score."""
    if score >= 7:
        return "#FF4B4B"  # Rouge (Urgence)
    elif score >= 4:
        return "#FFA500"  # Orange (Modéré)
    else:
        return "#4CAF50"  # Vert (Stable)

def generate_pdf(patient_name, diagnosis):
    """Génère un PDF contenant le diagnostic du patient."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Diagnostic de {patient_name}", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, diagnosis)
    pdf_output = f"rapport_{patient_name}.pdf"
    pdf.output(pdf_output)
    return pdf_output

def calculate_health_score(response_list, scores_to_coefs):
    sum_responses = [sum(response_list[i:i+5]) for i in range(0, 25, 5)]
    return max(0, min(10, 10 * (1 - sum([scores_to_coefs[score-1][i] for i, score in enumerate(sum_responses)]))))

# Coefficients pour le calcul des scores
score_to_coefs_MO = [0, 0.03759, 0.04774, 0.17949, 0.32509]
score_to_coefs_SC = [0, 0.03656, 0.050781, 0.172251, 0.258331]
score_to_coefs_UA = [0, 0.03313, 0.03979, 0.15689, 0.24005]
score_to_coefs_PD = [0, 0.02198, 0.04704, 0.26374, 0.44399]
score_to_coefs_AD = [0, 0.02046, 0.04683, 0.20005, 0.25803]

scores_to_coefs = np.array(list(zip(score_to_coefs_MO, score_to_coefs_SC, score_to_coefs_UA, score_to_coefs_PD, score_to_coefs_AD)))

patients = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
patient_responses = {name: np.random.randint(0, 2, 25).tolist() for name in patients}
patient_scores = {name: calculate_health_score(responses, scores_to_coefs) for name, responses in patient_responses.items()}

# Trier les scores par ordre décroissant
sorted_patients = sorted(patient_scores.items(), key=lambda x: x[1], reverse=True)

def main():
    st.title("👨‍⚕️ Doctor Interface")
    
    tabs = st.tabs(["📋 Priorité des Patients", "📝 Diagnostic & PDF"])
    
    with tabs[0]:
        st.header("Liste des patients classés par priorité")

        for name, score in sorted_patients:
            file_name = f"rapport_{name}.pdf"
            diagnosis = f"Compte-rendu médical de {name}.\nÉtat du patient analysé avec un score de {score:.2f}/10."
            color = color_code(score)

            st.markdown(
                f"""
                <div style="
                    background-color: {color}; 
                    color: white; 
                    padding: 8px; 
                    margin: 8px 0; 
                    border-radius: 10px; 
                    text-align: center; 
                    font-size: 16px; 
                    font-weight: bold;
                ">
                    {name} : Score = {score:.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander(f"📋 Voir le compte-rendu de {name}"):
                st.write(diagnosis)
                pdf_file = generate_pdf(name, diagnosis)
                with open(pdf_file, "rb") as file:
                    st.download_button(label="📥 Télécharger le PDF", data=file, file_name=pdf_file, mime="application/pdf")

    with tabs[1]:  # Onglet Diagnostic & PDF
        st.header("📝 Rédiger un diagnostic")
        patient_name = st.selectbox("Sélectionnez un patient", ["Alice", "Bob", "Charlie", "David", "Emma"])
        diagnosis_text = st.text_area("Écrivez le diagnostic ici")
        
        if st.button("📄 Générer et Envoyer PDF"):
            pdf_file = generate_pdf(patient_name, diagnosis_text)
            with open(pdf_file, "rb") as file:
                st.download_button(label="📥 Télécharger le PDF", data=file, file_name=pdf_file, mime="application/pdf")
            st.success(f"📄 PDF généré et envoyé pour {patient_name} !")

if __name__ == "__main__":
    main()
