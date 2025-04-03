import random

CONSTRAINT_LIST = [
    # "inversion",
    # "separable verb",
    "noun",
    "adjective",
    # "adverb phrase",
    # "conjunction",
    # "preposition",
    "interjection",
    # "article",
    "pronoun",
    # "determiner",
    "present tense",
    # "past tense",
    # "future tense",
    # "conditional tense",
    "imperative",
    # "subjunctive",
    # "gerund",
    "something about the weather",
    "something about the time of day",
    "something about a place",
    "something about a person",
    # "something about the thing",
    "something about an animal",
    # "something about the plant",
    # "something about an object",
    # "something about an activity",
    # "something about an emotion",
    # "something about a thought"
]

language_selection = ("Dutch", "English")

def get_learning_language():
    print("getting learning language")
    print(language_selection[0])
    return language_selection[0]

def get_understanding_language():
    print("getting understanding language")
    print(language_selection[1])
    return language_selection[1]

def set_understanding_language(language: str):
    global language_selection
    language_selection = (get_learning_language(), language)

def set_learning_language(language: str):
    global language_selection
    language_selection = (language, get_understanding_language())

def get_constraints():
    return random.sample(CONSTRAINT_LIST, 3)

def get_supported_languages():
    return [
        "English",
        "Dutch",
        # "French",
        # "German",
        # "Spanish",
        # "Italian",
        # "Portuguese",
        # "Russian",
        "Chinese",
        # "Japanese",
        # "Korean",
        # "Vietnamese",
        # "Arabic",
        # "Turkish",
        # "Polish",
        # "Czech",
        # "Hungarian",
        # "Romanian",
        # "Bulgarian",
        # "Greek",
        # "Hebrew",
        # "Hindi",
        # "Indonesian",
        # "Malay",
        # "Thai",
        # "Klingon",
        # "Elvish",
        # "Dothraki",
        # "Norse",
        # "Old English",
        # "Old French",
    ]