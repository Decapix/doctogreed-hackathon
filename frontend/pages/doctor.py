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


def sum_domain_scores(response_dict):

    sum_physical_limitations = sum([response_dict[str(i)][0] for i in [1, 2, 3]])
    sum_symptom_frequency = sum([response_dict[str(i)][0] for i in [5, 6]])
    sum_symptom_burden = sum([response_dict[str(i)][0] for i in [4, 7]])
    sum_quality_of_life = sum([response_dict[str(i)][0] for i in [8, 9]])
    sum_social_limitations = sum([response_dict[str(i)][0] for i in [10, 11, 12]])
    
    return [sum_physical_limitations, sum_symptom_frequency, sum_symptom_burden, sum_quality_of_life, sum_social_limitations]


def calculate_transformed_score(sum_of_items, min_possible_sum, max_possible_sum):
    """
    Calculate the transformed score on a 0-100 scale.

    Parameters:
    sum_of_items (int): The sum of the item scores for the domain.
    min_possible_sum (int): The minimum possible sum for the domain.
    max_possible_sum (int): The maximum possible sum for the domain.

    Returns:
    float: The transformed score on a 0-100 scale.
    """
    if sum_of_items < min_possible_sum or sum_of_items > max_possible_sum:
        raise ValueError("Sum of items is out of the possible range.")

    transformed_score = ((sum_of_items - min_possible_sum) /
                        (max_possible_sum - min_possible_sum)) * 100
    return transformed_score


def calculate_total_score(patient_dict):
    """
    Calculate the total score across all domains.

    Parameters:
    physical_limitations_sum (int): Sum of scores for Physical Limitations items.
    symptom_frequency_sum (int): Sum of scores for Symptom Frequency items.
    symptom_burden_sum (int): Sum of scores for Symptom Burden items.
    quality_of_life_sum (int): Sum of scores for Quality of Life items.
    social_limitations_sum (int): Sum of scores for Social Limitations items.

    Returns:
    float: The overall summary score.
    """
    physical_limitations_sum, symptom_frequency_sum, symptom_burden_sum, quality_of_life_sum, social_limitations_sum = sum_domain_scores(patient_dict["response"])
    min_max_values = {
        'physical_limitations': (3, 18),
        'symptom_frequency': (2, 14),
        'symptom_burden': (2, 10),
        'quality_of_life': (2, 10),
        'social_limitations': (3, 18)
    }
    patient_name = patient_dict["patient_name"]
    # Calculate transformed scores for each domain
    transformed_scores = {
        'physical_limitations': calculate_transformed_score(physical_limitations_sum, *min_max_values['physical_limitations']),
        'symptom_frequency': calculate_transformed_score(symptom_frequency_sum, *min_max_values['symptom_frequency']),
        'symptom_burden': calculate_transformed_score(symptom_burden_sum, *min_max_values['symptom_burden']),
        'quality_of_life': calculate_transformed_score(quality_of_life_sum, *min_max_values['quality_of_life']),
        'social_limitations': calculate_transformed_score(social_limitations_sum, *min_max_values['social_limitations'])
    }

    # Calculate the overall summary score
    overall_summary_score = sum(transformed_scores.values()) / len(transformed_scores)
    return {"patient_name": patient_name, "overall_summary_score": overall_summary_score}

data_patient1 = {
    "patient_name": "Monty Python",
    "patient_gender": 1,
    "responses": {
        "1": [1,1,5,"Extremely"],
        "2": [2,1,5,"Quite a bit"],
        "3": [1,1,5,"Moderately"],
        "4": [4,1,5,"Less than once a week"],
        "5": [1,1,7,"1-2 times per week"],
        "6": [6,1,5,"Less than once week"],
        "7": [5,1,5,"Never over the past 2 weeks"],
        "8": [1,1,5,"Slightly"],
        "9": [1,1,5,"Not at all satisfied"],
        "10": [3,1,5,"Moderately"],
        "11": [1,1,5,"Slightly"],
        "12": [2,1,5,"Quite a bit"]
    }
}

data_patient2 = {
    "patient_name":"Mindy Moon",
    "patient_gender": 0,
    "responses": {
        "1": [1,1,5,"Extremely"],
        "2": [2,1,5,"Quite a bit"],
        "3": [1,1,5,"Moderately"],
        "4": [1,1,5,"Every morning"],
        "5": [1,1,7,"1-2 times per week"],
        "6": [6,1,5,"Less than once week"],
        "7": [5,1,5,"Never over the past 2 weeks"],
        "8": [1,1,5,"Slightly"],
        "9": [1,1,5,"Not at all satisfied"],
        "10": [5,1,5,"Not at all"],
        "11": [1,1,5,"Slightly"],
        "12": [2,1,5,"Quite a bit"]
    }
}

def create_score_dictionary_list(list, new_dict):
    list.append(new_dict)
    

def rank_patients(list_of_patient_score_dicts):
    """
    Rank patients based on their overall summary scores.

    Parameters:
    list_of_patient_score_dicts (list): A list of dictionaries containing patient names and their overall summary scores.

    Returns:
    list: A list of tuples containing patient names and their overall summary scores, sorted in descending order of scores.
    """
    sorted_patients = sorted(list_of_patient_score_dicts, key=lambda x: x['overall_summary_score'], reverse=False)
    return sorted_patients


def main():
    list_patient_score_dicts = []

    st.title("👨‍⚕️ Doctor Interface")
    
    tabs = st.tabs(["📋 Priorité des Patients", "📝 Diagnostic & PDF"])
    
    with tabs[0]:
        st.header("Liste des patients classés par priorité")
        # where is patient data ???
        create_score_dictionary_list(list_patient_score_dicts, calculate_total_score(data_patient1))
        sorted_patients = rank_patients(list_patient_score_dicts)
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