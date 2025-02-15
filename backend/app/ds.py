from openai import OpenAI
import json
from io import StringIO

client = OpenAI(
    base_url = "https://api.scaleway.ai/c98de2b2-feb7-4780-a578-4c5276194bf4/v1",
	api_key = "a1a533f0-283e-4977-b763-2759d25e1f7f"
)

def askQuestion(question, language, gender):
    response = client.chat.completions.create(
        model="mistral-nemo-instruct-2407",
        messages=[
            { "role": "system", "content": "You are an AI assistant. You will ask me back the question I am giving to you." + "Ask it in " + language + ". You are talking to a " + gender +", keep it medical and neutral."},
            { "role": "user", "content": question },
        ],
        max_tokens=512,
        temperature=0.6,
        top_p=0.95,
        presence_penalty=0,
        stream=True,
    )
    return (response)

def receiveQuestion(response):
    output = StringIO()
    for chunk in response:
        if chunk.choices and chunk.choices[-1].delta.content:
            output.write(chunk.choices[-1].delta.content)
    return output.getvalue()

def take_question(file):
    for question in file:
        tmp = askQuestion(question['text'], "english", "female")
        question['text'] =  receiveQuestion(tmp)
    return (file)
