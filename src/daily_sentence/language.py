import random

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Dutch": "nl",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
}

CONSTRAINT_LIST = [
    # "inversion",
    # "separable verb",
    "noun",
    "adjective",
    "adverb or adverb phrase",
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
    "something about an activity",
    # "something about an emotion",
    "something about a thought"
]

class LanguageSelection:

    def __init__(self, learning_language: str, understanding_language: str):
        # Store both name and code
        self.learning_language_name = learning_language
        self.understanding_language_name = understanding_language
        self.learning_language_code = SUPPORTED_LANGUAGES[learning_language]
        self.understanding_language_code = SUPPORTED_LANGUAGES[understanding_language]

    def get_learning_language(self) -> str:
        """Get display name of learning language"""
        return self.learning_language_name

    def get_understanding_language(self) -> str:
        """Get display name of understanding language"""
        return self.understanding_language_name

    def get_learning_language_code(self) -> str:
        """Get ISO code of learning language"""
        return self.learning_language_code

    def get_understanding_language_code(self) -> str:
        """Get ISO code of understanding language"""
        return self.understanding_language_code

    def set_learning_language(self, learning_language: str):
        self.learning_language_name = learning_language
        self.learning_language_code = SUPPORTED_LANGUAGES[learning_language]

    def set_understanding_language(self, understanding_language: str):
        self.understanding_language_name = understanding_language
        self.understanding_language_code = SUPPORTED_LANGUAGES[understanding_language]

    
def get_constraints():
    return random.sample(CONSTRAINT_LIST, 3)

def get_supported_languages():
    """Get list of supported language names for UI and ChatGPT"""
    return list(SUPPORTED_LANGUAGES.keys())