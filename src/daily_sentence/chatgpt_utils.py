from openai import OpenAI
from language import get_learning_language, get_understanding_language, get_supported_languages
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

localization_cache = {
    "Dutch": {
        "English": "Engels",
        "Dutch": "Nederlands",
        "Chinese": "Chinees",
        "French": "Frans",
        "German": "Duits",
        "Italian": "Italiaans",
        "Portuguese": "Portugees",
    },
}

def as_translator(sentence: str, learning_language: str, understanding_language: str, context: str):
    sentence_pieces = re.split(r'\w+', sentence)

    if context:
        context_str = f"using the context {context}, " 
    else:
        context_str = ""

    prompt = f"""
    act as a translator.  {context_str}translate the following phrase, sentence or word after the dashes from {learning_language} to {understanding_language}, without any additional commentary:
    ----
    {sentence}
    """
    return get_completion(prompt)

def as_language_name(language_name: str, understanding_language: str):
    prompt = f"""
    what is the word {language_name} (language name) in {understanding_language} (without any additional commentary)?
    """
    return get_completion(prompt)

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
    
    Please use the following form for a response, and include no other commentary:

    [boolean, "string", "string", "string", "string"]

    the sentence:
    
    {sentence}
    """

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

def get_localized_string(english_string: str, understanding_language: str, context: str = None):
    if understanding_language == "English":
        return english_string
    elif english_string in get_supported_languages():
        return as_language_name(english_string, understanding_language)
    else:
        if localization_cache.get(understanding_language) is None:
            localization_cache[understanding_language] = {}
        if localization_cache[understanding_language].get(english_string) is None:
            localization_cache[understanding_language][english_string] = as_translator(english_string, "English", understanding_language, context)
        return localization_cache[understanding_language][english_string]