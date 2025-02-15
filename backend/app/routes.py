from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import logging as log
from typing import List, Literal, Optional
from db_models import *
from enter_model import *
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from ds import take_question
from diago import interview_summup

router = APIRouter()

@router.post("/create/patient/")
async def create_patient(patient_request: PatientCreateRequest):
    patient = await Patient.create(nom=patient_request.nom)
    return patient.nom


@router.post("/create/docteur/")
async def create_docteur(docteur_request: PatientCreateRequest):
    docteur = await Docteur.create(nom=docteur_request.nom)
    return docteur.nom



# Route GET /diagnostic
@router.get("/diagnostic", response_model=List[Question]) # envoyer les question au frontend
async def get_diagnostic_questions():
    """
    Renvoie une liste de questions pour le diagnostic.
    Chaque question inclut le type de réponse attendu (boolean ou scale).
    Pour les questions de type "scale", un intervalle (range) est également fourni.
    """
    question = take_question(questions)
    return question



@router.post("/recup-diagnostic/", status_code=status.HTTP_200_OK)
async def create_diagnostic(data: DiagnosticData):
    log.error(f"Received diagnostic data: {data}")
    try:
        patient = await Patient.get(nom=data.patient_name)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Transformation des réponses
    responses = {}
    for key, value in data.responses.items():
        # Split the string into a list of values
        response_values = value.split(", ")
        # Convert the first three values to integers
        response_values[:3] = [int(v) for v in response_values[:3]]
        # Add the response to the responses dictionary
        responses[int(key)] = response_values

    # Création du dictionnaire file
    file = {
        "patient_name": data.patient_name,
        "patient_gender": "male" if data.patient_gender == 1 else "female",
        "responses": responses
    }

    # Appel de la fonction interview_summup avec les bonnes entrées
    res = interview_summup(3.24, file)

    diagnostic = await Diagnostic.create(
        contenu={"responses": res},
        questions=questions,
        patient=patient,
        genre=data.patient_gender
    )

    return {"message": "Diagnostic recorded successfully"}


@router.get("/get_diagnostique/", response_model=List[DiagnosticResponse]) # le frontend docteur me demande le resultat du diagnostic
async def get_diagnostics():
    # Using Prefetch to optimize the database access and get the related patient name
    diagnostics = await Diagnostic.all().prefetch_related(
        Prefetch("patient", queryset=Patient.all().only("id", "nom"))
    )

    response = []
    for diagnostic in diagnostics:
        # Building the response ensuring to include only the patient's name
        response.append({
            "genre": diagnostic.genre,
            "contenu": diagnostic.contenu,
            "questions": diagnostic.questions,
            "patient_name": diagnostic.patient.nom
        })

    return response



@router.get("/home")
async def read_data(n: int = 10):
    """ok"""
    return {"ok": "ok"}
