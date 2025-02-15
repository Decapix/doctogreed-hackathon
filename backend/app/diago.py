from openai import OpenAI
import json
from io import StringIO

client = OpenAI(
    base_url = "https://api.scaleway.ai/c98de2b2-feb7-4780-a578-4c5276194bf4/v1",
    api_key = "a1a533f0-283e-4977-b763-2759d25e1f7f"
)

def dictDataExtract(file):
    result = "Patient name: " + file['patient_name'] + ", gender: " + file['patient_gender'] + "\n"
    key = 2
    for key, value in file["responses"].items():
        result += "Questions: " + value[4] + " answer: " + value[3] + "\n"
    return result

def mistral_summup(score, file, language):
    prompt = dictDataExtract(file)
    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages = [
            { "role": "system", "content": "This data is compose of " + prompt + ". Use only does data and the score given by the users, be neutral. Give exactly the answers to the question but in " + language + ". Try to structure correctly the answer."},
            { "role": "user", "content": "Give me a sum up in " + language + "of the patient interview according to his response. His calculate emergency score is : " + str(score) + " The emergency score is on a scale to 10, tell me if the score is low medium or high."},
        ],
        max_tokens=512,
        temperature=0.3,
        top_p=1,
        presence_penalty=0,
        stream=True,
    )
    return (response)

def interview_summup(score, file):
    language = "french"
    result = StringIO()
    response = mistral_summup(score, file, language)
    for chunk in response:
        if chunk.choices and chunk.choices[-1].delta.content:
            result.write(chunk.choices[-1].delta.content)
    return result.getvalue()

"""test = {
    "patient_name": "Louis Martin",
    "patient_gender": "male",
    "responses": {
        1: [1, 1, 5, "pas beaucoup", "des problemes cardiaques ?"],
        2: [0, 1, 1, "non", "des traitements reguliers ?"],
        3: [4, 1, 5, "tres regulierement", "des difficultes respiratoires ?"],
    },
}

score = 3.4
sum_up = interview_summup(score, test)
print(sum_up)"""

