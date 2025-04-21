from openai import OpenAI
from language import get_supported_languages, SUPPORTED_LANGUAGES
from translation_api import TranslationApiClient
from nicegui import ui
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

translation_api = TranslationApiClient()

localization_cache = {
    "Dutch": {
        "English": "Engels",
        "Dutch": "Nederlands",
        "Chinese": "Chinees",
        "French": "Frans",
        "German": "Duits",
        "Italian": "Italiaans",
    },
}

def show_error_dialog():
    """Show error dialog with reload button"""
    with ui.dialog() as dialog, ui.card():
        ui.label('Failed to load translations. Please try again.')
        with ui.row():
            ui.button('Reload', on_click=lambda: (dialog.close(), ui.refresh()))

def as_translator(sentence: str, learning_language: str, understanding_language: str, context: str):
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

def analyze_sentence(sentence: str, learning_language: str, understanding_language: str, constraints: list[str]):
    prompt = construct_teacher_prompt(sentence, learning_language, understanding_language, construct_constraint_string(constraints))
    return get_completion(prompt)

def get_localized_string(english_string: str, understanding_language: str, context: str = None):
    """Get localized UI strings using the Translation API as cache"""
    if understanding_language == "English":
        return english_string
    
    if english_string in get_supported_languages():
        context = " as a language name"

    try:
        result = translation_api.translate(
            source_text=english_string,
            source_language=SUPPORTED_LANGUAGES["English"],
            target_language=SUPPORTED_LANGUAGES[understanding_language],
            source_context=context
        )
        if result and 'result' in result:
            return result['result']
    except Exception as e:
        print(f"Translation API failed: {e}")
        show_error_dialog()
        return english_string  # Fallback to English until reload

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