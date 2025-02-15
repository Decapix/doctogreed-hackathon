from enter_model import *


def get_question_text(question_id):
    for question in questions:
        if question['id'] == question_id:
            return question['text']
    return "Question non trouvée."
