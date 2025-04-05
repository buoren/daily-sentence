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
    "in the present",
    "in the past",
    "in the future",
    "polite",
    "imperative",
    "familiar",
    # "gerund",
    "something about the weather",
    "something about the time of day",
    "something about a place",
    "something about a person",
    # "something about the thing",
    "something about an animal",
    "something about the plant",
    # "something about an object",
    # "something about an activity",
    # "something about an emotion",
    "something about a thought"
]

class LanguageSelection:

    def __init__(self, learning_language: str, understanding_language: str):
        self.learning_language = learning_language
        self.understanding_language = understanding_language

    def get_learning_language(self):
        return self.learning_language

    def get_understanding_language(self):
        return self.understanding_language  

    def set_learning_language(self, learning_language: str):
        self.learning_language = learning_language

    def set_understanding_language(self, understanding_language: str):
        self.understanding_language = understanding_language

    
def get_constraints():
    return random.sample(CONSTRAINT_LIST, 3)

def get_supported_languages():
    return [
        "English",
        "Dutch",
        "French",
        "German",
        "Spanish",
        "Italian",
        # "Portuguese",
        # "Russian",
        "Chinese",
        "Japanese",
        # "Korean",
        # "Vietnamese",
        "Arabic",
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