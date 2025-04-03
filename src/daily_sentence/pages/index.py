from nicegui import ui
from daily_sentence.language import get_constraints, get_supported_languages, get_learning_language, get_understanding_language, set_understanding_language, set_learning_language
from daily_sentence.chatgpt_utils import analyze_sentence, get_localized_string
from collections.abc import Callable

def construct_input_card():
    label_text = get_localized_string("Write your sentence here", get_understanding_language())
    placeholder_text = get_localized_string("Enter your sentence...", get_understanding_language())
    user_input = ui.textarea(label_text, placeholder=placeholder_text).classes('w-full mt-4')        
    result_container = ui.element('div').classes('w-full mt-4')
    return (user_input, result_container)

def construct_constraints_card():
    practice_cta = get_localized_string(f"Write today's {get_learning_language()} practice sentence using:", get_understanding_language())
    ui.label(practice_cta).classes('text-2xl font-bold mb-6 w-full text-center')
    constraints = get_constraints()
    constraint_cards = []
    for i, constraint in enumerate(constraints, 1):
        constraint_text = get_localized_string(constraint, get_understanding_language())
        constraint_label = ui.label(f"{i}. {constraint_text}").classes('text-lg mb-3 w-full text-center')
        constraint_cards.append(constraint_label)
    ui.separator().classes('my-4')
    return constraints, constraint_cards

def reconstitute_constraint_cards(constraint_cards: list[ui.element]):
    new_constraints = get_constraints()
    for i, constraint in enumerate(new_constraints, 1):
        constraint_text = get_localized_string(constraint, get_understanding_language())
        constraint_cards[i-1].text = f"{i}. {constraint_text}"
    return new_constraints, constraint_cards

def construct_language_card(language_function: Callable[[str, str], None]):
    language_card = ui.card().classes('w-96 p-4 bg-white shadow-lg text-center')
    with language_card:
        languages = get_supported_languages()
        translated_languages = {}
        my_language = get_understanding_language()
        to_language = get_learning_language()
        for language in languages:
            for_my_language = ""
            if language == my_language:
                for_my_language = f" for {my_language}"
            translated_languages[language] = get_localized_string(language, get_understanding_language(), f"of a language name {for_my_language}")
        with ui.row().classes('w-full justify-center'):
            language_cta = get_localized_string("I understand %s." % my_language, my_language)
            with ui.dropdown_button(language_cta, value=my_language, auto_close=True).classes('w-full'):
                for language in languages:
                    def make_handler(lang=language):
                        def handler():
                            language_function(f"{to_language}:{lang}")
                            create_language_main_card.refresh()
                        return handler
                    ui.item(translated_languages[language], on_click=make_handler())
            
            to_language_cta = get_localized_string("I want to learn %s." % to_language, my_language)
            with ui.dropdown_button(to_language_cta, value=to_language, auto_close=True).classes('w-full'):
                for language in languages:
                    def make_handler(lang=language):
                        def handler():
                            language_function(f"{lang}:{my_language}")
                            create_language_main_card.refresh()
                        return handler
                    ui.item(translated_languages[language], on_click=make_handler())
    print("created language card")
    return language_card

def fill_main_card(main_card: ui.element):
    with main_card:
        constraints, constraint_cards = construct_constraints_card()
        user_input, result_container = construct_input_card()

        def process_click():
            result_container.classes('transition delay-150 duration-300 ease-in-out opacity-100')
            sentence = user_input.value
            user_input.clear()
            chatgpt_response = analyze_sentence(sentence, get_learning_language(), get_understanding_language(), constraints)
            chatgpt_response = chatgpt_response.replace('true', 'True').replace('false', 'False')
            (success, explanation, original, proper, proper_translated) = list(eval(chatgpt_response))
            with result_container:
               with ui.card().classes('bg-gray-50 p-4'):
                    with ui.card():
                        with ui.row().classes('text-3xl'):
                            ui.icon('check_circle', color='green') if success else ui.icon('cancel', color='red')
                            ui.label(sentence)
                        with ui.row():
                            translated_label_str = get_localized_string("Translated", get_understanding_language())
                            ui.label(f"{translated_label_str}: {original}")
                    with ui.card():
                        ui.label(explanation)
                        ui.label(proper)
                        ui.label(proper_translated)

        def on_submit():
            result_container.clear()
            ui.timer(.5, process_click, once=True)

        def on_new_constraints():
            nonlocal constraints, constraint_cards
            result_container.clear()
            user_input.clear()
            constraints, constraint_cards = reconstitute_constraint_cards(constraint_cards)
        
        make_buttons(on_submit, on_new_constraints)
        print("filled main card")

def make_buttons(on_submit: Callable[[], None], on_new_constraints: Callable[[], None]):
    submit_str = get_localized_string('Check', get_understanding_language(), context="a button to check the correctness of a sentence by a student")
    new_constraints_str = get_localized_string('New constraints', get_understanding_language(), context="a button to get three new constraints for the sentence by a student")
    with ui.row().classes('w-full justify-center'):
        ui.button(new_constraints_str, on_click=on_new_constraints).classes('mt-4 bg-secondary')
        ui.button(submit_str, on_click=on_submit).classes('mt-4 bg-primary')
    print("made buttons")
        
def create_whole_page():
    with ui.column().classes('w-full h-screen items-center justify-center'):
        create_language_main_card()

@ui.refreshable
def create_language_main_card():
    print("creating language main card")
    language_pair, local_set_language = ui.state(f"Dutch:English")
    learning_language, understanding_language = language_pair.split(":")
    set_learning_language(learning_language)
    set_understanding_language(understanding_language)
    main_card = ui.card().classes('w-96 p-4 bg-white shadow-lg text-center')
    language_card = construct_language_card(local_set_language)
    fill_main_card(main_card)
    print("created whole page")


def main_page():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.query('body').classes('bg-sky-100')  # Light blue background for the whole page
    create_whole_page()

