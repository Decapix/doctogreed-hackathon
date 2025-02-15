from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field


# Liste de questions (Kansas City Cardiomyopathy Questionnaire (KCCQ-12))
questions = [
    {"id": 1, "text": "How much you are limited by shortness of breath or fatigue in your ability to shower/bathe?", "response_type": "scale", "range": {1:"Extremely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 2, "text": "How much you are limited by shortness of breath or fatigue in your ability to walk 1 block on level ground?", "response_type": "scale", "range": {1:"Extremely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 3, "text": "How much you are limited by shortness of breath or fatigue when hurrying or jogging?", "response_type": "scale", "range": {1:"Extremely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 4, "text": "Over the past 2 weeks, how many times did you have swelling in your feet, ankles or legs when you woke up in the morning?", "response_type": "scale", "range": {1:"Every morning", 2:"3 or more times per week but not every day", 3:"1-2 times per week", 4:"Less than once a week", 5:"Never over the past 2 weeks"}},
    {"id": 5, "text": "Over the past 2 weeks, on average, how many times has fatigue limited your ability to do what you wanted?", "response_type": "scale", "range": {1:"All of the time", 2:"Several times per day", 3:"At least once a day", 4:"3 or more times per week but not every day", 5:"1-2 times per week", 6:"Less than once week", 7:"Never over the past 2 weeks"}},
    {"id": 6, "text": "Over the past 2 weeks, on average, how many times has shortness of breath limited your ability to do what you wanted?", "response_type": "scale", "range": {1:"All of the time", 2:"Several times per day", 3:"At least once a day", 4:"3 or more times per week but not every day", 5:"1-2 times per week", 6:"Less than once week", 7:"Never over the past 2 weeks"}},
    {"id": 7, "text": "Over the past 2 weeks, on average, how many times have you been forced to sleep sitting up in a chair or with at least 3 pillows to prop you up because of shortness of breath?", "response_type": "scale", "range": {1:"Every morning", 2:"3 or more times per week but not every day", 3:"1-2 times per week", 4:"Less than once a week", 5:"Never over the past 2 weeks"}},
    {"id": 8, "text": "Over the past 2 weeks, how much have your symptoms limited your enjoyment of life?", "response_type": "scale", "range": {1:"Extremely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 9, "text": "If you had to spend the rest of your life with your symptoms the way they are right now, how would you feel about this?", "response_type": "scale", "range": {1:"Not at all satisfied", 2:"Mostly dissatisfied", 3:"Somewhat satisfied", 4:"Mostly satisfied", 5:"Completely satisfied"}},
    {"id": 10, "text": "How do your symptoms limit your hobbies and recreational activities?", "response_type": "scale", "range": {1:"Severely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 11, "text": "How do your symptoms limit your ability to work or do household chores?", "response_type": "scale", "range": {1:"Severely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
    {"id": 12, "text": "How do your symptoms limit your ability to visit your family or friends?", "response_type": "scale", "range": {1:"Severely", 2:"Quite a bit", 3:"Moderately", 4:"Slightly", 5:"Not at all"}},
]
# Modèle Pydantic pour une question
class Question(BaseModel):
    id: int
    text: str
    response_type: Literal["boolean", "scale"]  # Type de réponse attendu
    range: Optional[Dict[int, str]] = None  # Dictionnaire pour les réponses de type "scale"

class PatientCreateRequest(BaseModel):
    nom: str


class DiagnosticData(BaseModel):
    patient_name: str = Field(..., example="Felou")
    patient_gender: int = Field(..., example=1)
    responses: Dict[int, str] = Field(..., example={1: "coucou", 2:"salam", 3:"jemappellebizarre", 4:"jaiunprobleme", 5:"jeprendsdutemps"})


class DiagnosticResponse(BaseModel):
    id: int
    genre: int
    contenu: Dict[str, str]
    questions: Dict[int, str]
    patient_name: str

    class Config:
        orm_mode = True
