from nicegui import ui
from daily_sentence.language import get_constraints, get_supported_languages, LanguageSelection
from daily_sentence.chatgpt_utils import analyze_sentence, get_localized_string
from collections.abc import Callable

def construct_input_card(language_selection: LanguageSelection):
    label_text = get_localized_string("Write your sentence here", language_selection.get_understanding_language())
    placeholder_text = get_localized_string("Enter your sentence...", language_selection.get_understanding_language())
    user_input = ui.textarea(label_text, placeholder=placeholder_text).classes('w-full mt-4')        
    result_container = ui.element('div').classes('w-full mt-4')
    return (user_input, result_container)

def construct_constraints_card(language_selection: LanguageSelection):
    practice_cta = get_localized_string(f"Write today's {language_selection.get_learning_language()} practice sentence using:", language_selection.get_understanding_language())
    ui.label(practice_cta).classes('text-2xl font-bold mb-6 w-full text-center')
    constraints = get_constraints()
    constraint_cards = []
    for i, constraint in enumerate(constraints, 1):
        constraint_text = get_localized_string(constraint, language_selection.get_understanding_language())
        constraint_label = ui.label(f"{i}. {constraint_text}").classes('text-lg mb-3 w-full text-center')
        constraint_cards.append(constraint_label)
    ui.separator().classes('my-4')
    return constraints, constraint_cards

def reconstitute_constraint_cards(constraint_cards: list[ui.element], language_selection: LanguageSelection):
    new_constraints = get_constraints()
    for i, constraint in enumerate(new_constraints, 1):
        constraint_text = get_localized_string(constraint, language_selection.get_understanding_language())
        constraint_cards[i-1].text = f"{i}. {constraint_text}"
    return new_constraints, constraint_cards

def construct_language_card(main_card: ui.element, language_function: Callable[[str, str], None], language_selection: LanguageSelection):
    language_card = ui.card().classes('w-96 p-4 bg-white shadow-lg text-center')
    with language_card:
        languages = get_supported_languages()
        translated_languages = {}
        my_language = language_selection.get_understanding_language()
        to_language = language_selection.get_learning_language()
        for language in languages:
            for_my_language = ""
            if language == my_language:
                for_my_language = f" for {my_language}"
            translated_languages[language] = get_localized_string(language, language_selection.get_understanding_language(), f"of a language name {for_my_language}")
        with ui.row().classes('w-full justify-center'):
            language_cta = get_localized_string("I understand %s." % my_language, my_language)
            with ui.dropdown_button(language_cta, value=my_language, auto_close=True).classes('w-full'):
                for language in languages:
                    language_cta = get_localized_string("I understand %s." % language, language)
                    def make_handler(lang=language):
                        def handler():
                            language_function(f"{to_language}:{lang}")
                        return handler
                    ui.item(language_cta, on_click=make_handler())
            
            to_language_cta = get_localized_string("I want to learn %s." % to_language, my_language)
            with ui.dropdown_button(to_language_cta, value=to_language, auto_close=True).classes('w-full'):
                for language in languages:
                    def make_handler(lang=language):
                        def handler():
                            language_function(f"{lang}:{my_language}")
                        return handler
                    ui.item(translated_languages[language], on_click=make_handler())
    return language_card

def fill_main_card(main_card: ui.element, language_selection: LanguageSelection):
    with main_card:
        constraints, constraint_cards = construct_constraints_card(language_selection)
        user_input, result_container = construct_input_card(language_selection)

        def process_click():
            result_container.classes('transition delay-150 duration-300 ease-in-out opacity-100')
            sentence = user_input.value
            user_input.clear()
            chatgpt_response = analyze_sentence(
                sentence,
                language_selection.get_learning_language(),
                language_selection.get_understanding_language(),
                constraints
            )
            chatgpt_response = chatgpt_response.replace('true', 'True').replace('false', 'False')
            (success, explanation, original, proper, proper_translated) = list(eval(chatgpt_response))
            with result_container:
               with ui.card().classes('bg-gray-50 p-4'):
                    with ui.card():
                        with ui.row().classes('text-3xl'):
                            ui.icon('check_circle', color='green') if success else ui.icon('cancel', color='red')
                            ui.label(sentence)
                        with ui.row():
                            translated_label_str = get_localized_string("Translated", language_selection.get_understanding_language())
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
            user_input.value = ""
            user_input.clear()
            constraints, constraint_cards = reconstitute_constraint_cards(constraint_cards)
        
        make_buttons(on_submit, on_new_constraints, language_selection)

def make_buttons(on_submit: Callable[[], None], on_new_constraints: Callable[[], None], language_selection: LanguageSelection):
    submit_str = get_localized_string('Check', language_selection.get_understanding_language(), context="a button to check the correctness of a sentence by a student")
    new_constraints_str = get_localized_string('New constraints', language_selection.get_understanding_language(), context="a button to get three new constraints for the sentence by a student")
    with ui.row().classes('w-full justify-center'):
        ui.button(new_constraints_str, on_click=on_new_constraints).classes('mt-4 bg-secondary')
        ui.button(submit_str, on_click=on_submit).classes('mt-4 bg-primary')

@ui.refreshable
def create_language_main_card(language_selection: LanguageSelection):
    language_pair, local_set_language = ui.state(f"Dutch:English")
    learning_language, understanding_language = language_pair.split(":")
    language_selection.set_learning_language(learning_language)
    language_selection.set_understanding_language(understanding_language)
    main_card = ui.card().classes('w-96 p-4 bg-white shadow-lg text-center')
    language_card = construct_language_card(main_card, local_set_language, language_selection)
    fill_main_card(main_card, language_selection)

def create_whole_page():
    language_selection = LanguageSelection("Dutch", "English")
    with ui.column().classes('w-full h-full items-center justify-center'):
        create_language_main_card(language_selection)
        with ui.row().classes('w-full justify-center'):
            ui.label("Brought to you by ").classes('text-sm')
            ui.link("Kevin Shiue", "https://buoren.net").classes('text-sm')

@ui.page('/')
def main_page():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.query('body').classes('bg-sky-100')  # Light blue background for the whole page
    create_whole_page()

