from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field


# Liste de questions (Kansas City Cardiomyopathy Questionnaire (KCCQ-12))
questions = [
    {"id": 1, "text": "How much you are limited by shortness of breath or fatigue in your ability to shower/bathe?", "response_type": "scale", "range": [1, 5]},
    {"id": 2, "text": "How much you are limited by shortness of breath or fatigue in your ability to walk 1 block on level ground?", "response_type": "scale", "range": [1, 5]},
    {"id": 3, "text": "How much you are limited by shortness of breath or fatigue in your ability of hurrying or jogging?", "response_type": "scale", "range": [1, 5]},
    {"id": 4, "text": "Over the past 2 weeks, how many times did you have swelling in your feet, ankles or legs when you woke up in the morning?", "response_type": "scale", "range": [0, 5]},
    {"id": 5, "text": "Over the past 2 weeks, on average, how many times has fatigue limited your ability to do what you wanted?", "response_type": "scale", "range": [0, 5]},
    {"id": 6, "text": "Over the past 2 weeks, on average, how many times has shortness of breath limited your ability to do what you wanted?", "response_type": "scale", "range": [0, 5]},
    {"id": 7, "text": "Over the past 2 weeks, on average, how many times have you been forced to sleep sitting up in a chair or with at least 3 pillows to prop you up because of shortness of breath?", "response_type": "scale", "range": [0, 5]},
    {"id": 8, "text": "Over the past 2 weeks, how much has your heart failure limited your enjoyment of life?", "response_type": "scale", "range": [0, 5]},
    {"id": 9, "text": "If you had to spend the rest of your life with your heart failure the way it is right now, how would you feel about this?", "response_type": "scale", "range": [0, 5]},
    {"id": 10, "text": "How do your symptoms limit your hobbies and recreational activities?", "response_type": "scale", "range": [0, 5]},
    {"id": 11, "text": "How do your symptoms limit your ability to work or do household chores?", "response_type": "scale", "range": [0, 5]},
    {"id": 12, "text": "How do your symptoms limit your ability to visit your family or friends?", "response_type": "scale", "range": [0, 5]},
]
# Modèle Pydantic pour une question
class Question(BaseModel):
    id: int
    text: str
    response_type: Literal["boolean", "scale"]  # Type de réponse attendu
    range: Optional[List[int]] = None  # Intervalle pour les réponses de type "scale"

class PatientCreateRequest(BaseModel):
    nom: str


class DiagnosticData(BaseModel):
    patient_name: str = Field(..., example="Felou")
    patient_gender: str = Field(..., example="Homme")
    responses: Dict[str, str] = Field(..., example={"1": "Vrai", "2": "2", "3": "4"})


class DiagnosticResponse(BaseModel):
    id: int
    genre: str
    contenu: Dict[str, str]
    questions: Dict[str, str]
    patient_name: str

    class Config:
        orm_mode = True
