from nicegui import ui
from daily_sentence.language import get_constraints, get_learning_language, get_understanding_language
from daily_sentence.chatgpt_utils import analyze_sentence, get_localized_string

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

def main_page():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.query('body').classes('bg-sky-100')  # Light blue background for the whole page

    # Create a centered container
    with ui.column().classes('w-full h-screen items-center justify-center'):
        main_card = ui.card().classes('w-96 p-4 bg-white shadow-lg text-center')
        with main_card:
            constraints, constraint_cards = construct_constraints_card()
            user_input, result_container = construct_input_card()

            def process_click():
                result_container.classes('transition delay-150 duration-300 ease-in-out opacity-100')
                sentence = user_input.value
                user_input.clear()
                chatgpt_response = analyze_sentence(sentence, get_learning_language(), get_understanding_language(), constraints)
                chatgpt_response = chatgpt_response.replace('true', 'True').replace('false', 'False')
                print(chatgpt_response)
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

            def make_buttons():
                submit_str = get_localized_string('Check', get_understanding_language(), context="a button to check the correctness of a sentence by a student")
                new_constraints_str = get_localized_string('New constraints', get_understanding_language(), context="a button to get three new constraints for the sentence by a student")
                with ui.row():
                    ui.button(submit_str, on_click=on_submit).classes('mt-4')
                    ui.button(new_constraints_str, on_click=on_new_constraints).classes('mt-4')

            def on_new_constraints():
                nonlocal constraints, constraint_cards
                constraints, constraint_cards = reconstitute_constraint_cards(constraint_cards)

            make_buttons()


