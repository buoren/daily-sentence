from nicegui import ui
from daily_sentence.pages.base_page import BasePage
from daily_sentence.language import LanguageSelection

# Import get_localized_string with error handling
try:
    from daily_sentence.chatgpt_utils import get_localized_string
except ImportError:
    from ..chatgpt_utils import get_localized_string


class VocabularyPage(BasePage):
    """Vocabulary practice page - example of how to add new pages"""

    def get_title(self) -> str:
        return "Vocabulary"

    def get_icon(self) -> str:
        return "book"

    def render(self) -> ui.element:
        """Render the vocabulary page"""
        self.container = ui.card().classes('w-full max-w-2xl mx-auto p-6 bg-white shadow-lg')
        with self.container:
            self.render_content()
        return self.container

    def render_content(self):
        """Render the page content"""
        # Title
        title = get_localized_string("Vocabulary Practice", self.language_selection.get_understanding_language())
        ui.label(title).classes('text-3xl font-bold mb-6 w-full text-center text-gray-800')

        # Coming soon message
        with ui.card().classes('p-6 bg-blue-50 border-l-4 border-blue-500 text-center'):
            ui.icon('construction', size='3xl', color='blue').classes('mb-4')

            coming_soon = get_localized_string("Coming Soon!", self.language_selection.get_understanding_language())
            ui.label(coming_soon).classes('text-2xl font-semibold text-blue-700 mb-2')

            description = get_localized_string(
                "Vocabulary practice exercises will be available here soon. This page demonstrates how easy it is to add new features to the application.",
                self.language_selection.get_understanding_language()
            )
            ui.label(description).classes('text-gray-600 max-w-md mx-auto leading-relaxed')

        # Example content to show the structure
        with ui.card().classes('mt-6 p-4 bg-gray-50'):
            example_title = get_localized_string("Example Features Coming:", self.language_selection.get_understanding_language())
            ui.label(example_title).classes('text-lg font-semibold mb-3 text-gray-800')

            features = [
                "Flashcard reviews",
                "Spaced repetition system",
                "Word associations",
                "Audio pronunciation",
                "Usage examples"
            ]

            for feature in features:
                translated_feature = get_localized_string(feature, self.language_selection.get_understanding_language())
                with ui.row().classes('items-center mb-2'):
                    ui.icon('check_circle', color='green').classes('mr-2')
                    ui.label(translated_feature).classes('text-gray-700')
