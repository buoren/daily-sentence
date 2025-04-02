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
    return language_selection[0]

def get_understanding_language():
    return language_selection[1]

def get_constraints():
    return random.sample(CONSTRAINT_LIST, 3)