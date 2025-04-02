from openai import OpenAI
from language import get_learning_language, get_understanding_language
import re
import os

def get_api_key():

    if os.path.exists('.chatgpt-key'):
        with open('.chatgpt-key', 'r') as file:
            return file.read().strip()
    else:
        return os.environ['OPENAI_API_KEY']

client = OpenAI(
    api_key=get_api_key()
)

def construct_translator_prompt(sentence: str, learning_language: str, understanding_language: str):
    sentence_pieces = re.split(r'\w+', sentence)
    if len(sentence_pieces) > 1:
        fragment = "sentence"
    else:
        fragment = "word"

    prompt = f"""
    act as a translator.  translate the following {fragment} from {learning_language} to {understanding_language}, without any additional commentary:

    {sentence}
    """
    return prompt

def construct_teacher_prompt(sentence: str, learning_language: str, understanding_language: str, constraints: str):
    prompt = f"""
    act as a lenient and friendly {learning_language} teacher.  i'm a student learning {learning_language} as a second language, 
    and i've been given the instruction to create a sentence with {constraints}.
    The response starts with a boolean, true if the sentence meets the constraints, false otherwise.
    In {understanding_language}, if it's correct, explain what i have done and if it's not correct explain
    what I could have done or changed minimally to meet the constraints. 
    Next, a translation to {understanding_language} of what I said in the original input sentence.
    And then a proper {learning_language} example sentence.
    And then a translation to {understanding_language} of the proper {learning_language} example.
    
    Please use the following form for a response:

    [boolean, "string", "string", "string", "string"]

    the sentence:
    
    {sentence}
    """

    print(prompt)
    return prompt
    
def get_completion(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=False,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def construct_constraint_string(constraints: list[str]):
    return " and ".join(constraints)

def analyze_sentence(sentence: str, learning_language: str, understanding_language: str, constraints: list[str]):
    prompt = construct_teacher_prompt(sentence, learning_language, understanding_language, construct_constraint_string(constraints))
    return get_completion(prompt)

def get_translated_string(sentence: str, learning_language: str, understanding_language: str):
    prompt = construct_translator_prompt(sentence, learning_language, understanding_language)
    return get_completion(prompt)

def get_localized_string(english_string: str, understanding_language: str):
    if understanding_language == "English":
        return english_string
    else:
        return get_translated_string(english_string, get_learning_language(), understanding_language)