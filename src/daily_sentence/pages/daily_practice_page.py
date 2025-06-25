from nicegui import ui
from daily_sentence.pages.base_page import BasePage
from daily_sentence.language import get_constraints, LanguageSelection
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from daily_sentence.chatgpt_utils import analyze_sentence, get_localized_string
from typing import List, Callable


class DailyPracticePage(BasePage):
    """Daily sentence practice page"""

    def __init__(self, language_selection: LanguageSelection):
        super().__init__(language_selection)
        self.constraints = []
        self.constraint_cards = []
        self.user_input = None
        self.result_container = None

    def get_title(self) -> str:
        return "Daily Practice"

    def get_icon(self) -> str:
        return "edit"

    def render(self) -> ui.element:
        """Render the daily practice page"""
        self.container = ui.card().classes('w-full max-w-2xl mx-auto p-6 bg-white shadow-lg')
        with self.container:
            self.render_content()
        return self.container

    def render_content(self):
        """Render the page content"""
        # Title and constraints
        self.render_constraints_section()

        # Input section
        self.render_input_section()

        # Action buttons
        self.render_action_buttons()

    def render_constraints_section(self):
        """Render the constraints section"""
        practice_cta = get_localized_string(
            f"Write today's {self.language_selection.get_learning_language()} practice sentence using:",
            self.language_selection.get_understanding_language()
        )
        ui.label(practice_cta).classes('text-2xl font-bold mb-6 w-full text-center text-gray-800')

        # Generate new constraints if needed
        if not self.constraints:
            self.constraints = get_constraints()

        # Clear previous constraint cards
        self.constraint_cards = []

        # Create constraint cards
        constraint_container = ui.card().classes('mb-6 p-4 bg-blue-50 border-l-4 border-blue-500')
        with constraint_container:
            for i, constraint in enumerate(self.constraints, 1):
                constraint_text = get_localized_string(
                    constraint,
                    self.language_selection.get_understanding_language()
                )
                constraint_label = ui.label(f"{i}. {constraint_text}").classes(
                    'text-lg mb-2 w-full text-gray-700 font-medium'
                )
                self.constraint_cards.append(constraint_label)

        ui.separator().classes('my-4')

    def render_input_section(self):
        """Render the input section"""
        label_text = get_localized_string(
            "Write your sentence here",
            self.language_selection.get_understanding_language()
        )
        placeholder_text = get_localized_string(
            "Enter your sentence...",
            self.language_selection.get_understanding_language()
        )

        self.user_input = ui.textarea(
            label=label_text,
            placeholder=placeholder_text
        ).classes('w-full mt-4')

        self.result_container = ui.element('div').classes('w-full mt-4')

    def render_action_buttons(self):
        """Render the action buttons"""
        submit_str = get_localized_string(
            'Check',
            self.language_selection.get_understanding_language(),
            context="a button to check the correctness of a sentence by a student"
        )
        new_constraints_str = get_localized_string(
            'New constraints',
            self.language_selection.get_understanding_language(),
            context="a button to get three new constraints for the sentence by a student"
        )

        with ui.row().classes('w-full justify-center mt-6 space-x-4'):
            ui.button(
                new_constraints_str,
                on_click=self.on_new_constraints
            ).classes('px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors')

            ui.button(
                submit_str,
                on_click=self.on_submit
            ).classes('px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors')

    def on_submit(self):
        """Handle sentence submission"""
        if not self.user_input or not self.user_input.value.strip():
            return

        self.result_container.clear()
        ui.timer(0.5, self.process_sentence, once=True)

    def process_sentence(self):
        """Process the submitted sentence"""
        sentence = self.user_input.value.strip()
        self.user_input.clear()

        # Show loading state
        with self.result_container:
            with ui.card().classes('bg-blue-50 p-4 text-center'):
                ui.spinner(size='lg').classes('mb-2')
                loading_text = get_localized_string(
                    "Analyzing your sentence...",
                    self.language_selection.get_understanding_language()
                )
                ui.label(loading_text).classes('text-gray-600')

        # Get ChatGPT response
        try:
            chatgpt_response = analyze_sentence(
                sentence,
                self.language_selection.get_learning_language(),
                self.language_selection.get_understanding_language(),
                self.constraints
            )

            # Parse response
            chatgpt_response = chatgpt_response.replace('true', 'True').replace('false', 'False')
            success, explanation, original, proper, proper_translated = list(eval(chatgpt_response))

            # Clear loading and show results
            self.result_container.clear()
            self.render_results(sentence, success, explanation, original, proper, proper_translated)

        except Exception as e:
            self.result_container.clear()
            with self.result_container:
                with ui.card().classes('bg-red-50 p-4 border-l-4 border-red-500'):
                    ui.icon('error', color='red').classes('mb-2')
                    error_text = get_localized_string(
                        "Sorry, there was an error analyzing your sentence. Please try again.",
                        self.language_selection.get_understanding_language()
                    )
                    ui.label(error_text).classes('text-red-700')

    def render_results(self, sentence: str, success: bool, explanation: str, original: str, proper: str, proper_translated: str):
        """Render the analysis results"""
        with self.result_container:
            with ui.card().classes('bg-gray-50 p-4 border-l-4 border-green-500' if success else 'bg-gray-50 p-4 border-l-4 border-orange-500'):
                # Header with success indicator
                with ui.card().classes('mb-4 p-3'):
                    with ui.row().classes('items-center mb-2'):
                        if success:
                            ui.icon('check_circle', color='green').classes('text-2xl mr-2')
                            status_text = get_localized_string("Great job!", self.language_selection.get_understanding_language())
                        else:
                            ui.icon('info', color='orange').classes('text-2xl mr-2')
                            status_text = get_localized_string("Almost there!", self.language_selection.get_understanding_language())
                        ui.label(status_text).classes('text-lg font-semibold')

                    ui.label(f'"{sentence}"').classes('text-xl italic text-gray-700')

                    if original:
                        translated_label = get_localized_string("Translation", self.language_selection.get_understanding_language())
                        ui.label(f"{translated_label}: {original}").classes('text-sm text-gray-600')

                # Explanation and correction
                with ui.card().classes('p-3'):
                    ui.label(explanation).classes('mb-3 text-gray-700 leading-relaxed')

                    if proper and proper != sentence:
                        suggestion_label = get_localized_string("Suggested improvement", self.language_selection.get_understanding_language())
                        ui.label(suggestion_label).classes('font-semibold text-gray-800 mb-1')
                        ui.label(f'"{proper}"').classes('text-lg italic text-blue-700 mb-2')

                        if proper_translated:
                            ui.label(f"({proper_translated})").classes('text-sm text-gray-600')

    def on_new_constraints(self):
        """Handle new constraints request"""
        self.result_container.clear()
        if self.user_input:
            self.user_input.value = ""
            self.user_input.clear()

        # Generate new constraints
        self.constraints = get_constraints()

        # Update constraint cards
        for i, constraint in enumerate(self.constraints, 1):
            constraint_text = get_localized_string(
                constraint,
                self.language_selection.get_understanding_language()
            )
            if i <= len(self.constraint_cards):
                self.constraint_cards[i-1].text = f"{i}. {constraint_text}"

    def on_language_changed(self):
        """Handle language change"""
        super().on_language_changed()
