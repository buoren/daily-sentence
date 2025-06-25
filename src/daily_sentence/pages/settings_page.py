from nicegui import ui
from daily_sentence.pages.base_page import BasePage
from daily_sentence.language import LanguageSelection, get_supported_languages

# Import get_localized_string with error handling
try:
    from daily_sentence.chatgpt_utils import get_localized_string
except ImportError:
    from ..chatgpt_utils import get_localized_string


class SettingsPage(BasePage):
    """Settings and preferences page"""

    def get_title(self) -> str:
        return "Settings"

    def get_icon(self) -> str:
        return "settings"

    def render(self) -> ui.element:
        """Render the settings page"""
        self.container = ui.card().classes('w-full max-w-2xl mx-auto p-6 bg-white shadow-lg')
        with self.container:
            self.render_content()
        return self.container

    def render_content(self):
        """Render the page content"""
        # Title
        title = get_localized_string("Settings", self.language_selection.get_understanding_language())
        ui.label(title).classes('text-3xl font-bold mb-6 w-full text-center text-gray-800')

        # Language Settings Section
        self.render_language_settings()

        # Application Settings Section
        self.render_app_settings()

        # About Section
        self.render_about_section()

    def render_language_settings(self):
        """Render language configuration section"""
        with ui.card().classes('mb-6 p-4'):
            section_title = get_localized_string("Language Settings", self.language_selection.get_understanding_language())
            ui.label(section_title).classes('text-xl font-semibold mb-4 text-gray-800')

            # Current language display
            learning_lang = self.language_selection.get_learning_language()
            understanding_lang = self.language_selection.get_understanding_language()

            with ui.row().classes('w-full justify-between items-center mb-3'):
                learning_label = get_localized_string("Learning Language", understanding_lang)
                ui.label(f"{learning_label}:").classes('font-medium text-gray-700')
                ui.label(learning_lang).classes('text-blue-600 font-medium')

            with ui.row().classes('w-full justify-between items-center mb-4'):
                understanding_label = get_localized_string("Interface Language", understanding_lang)
                ui.label(f"{understanding_label}:").classes('font-medium text-gray-700')
                ui.label(understanding_lang).classes('text-blue-600 font-medium')

            # Language selection
            languages = get_supported_languages()

            with ui.row().classes('w-full space-x-4'):
                # Learning language selector
                with ui.column().classes('flex-1'):
                    learning_select_label = get_localized_string("Change Learning Language", understanding_lang)
                    ui.label(learning_select_label).classes('text-sm font-medium text-gray-600 mb-1')
                    learning_select = ui.select(
                        languages,
                        value=learning_lang,
                        on_change=lambda e: self.language_selection.set_learning_language(e.value)
                    ).classes('w-full')

                # Understanding language selector
                with ui.column().classes('flex-1'):
                    interface_select_label = get_localized_string("Change Interface Language", understanding_lang)
                    ui.label(interface_select_label).classes('text-sm font-medium text-gray-600 mb-1')
                    interface_select = ui.select(
                        languages,
                        value=understanding_lang,
                        on_change=lambda e: self.on_interface_language_change(e.value)
                    ).classes('w-full')

    def render_app_settings(self):
        """Render application settings section"""
        with ui.card().classes('mb-6 p-4'):
            section_title = get_localized_string("Application Settings", self.language_selection.get_understanding_language())
            ui.label(section_title).classes('text-xl font-semibold mb-4 text-gray-800')

            # Theme setting (placeholder)
            with ui.row().classes('w-full justify-between items-center mb-3'):
                theme_label = get_localized_string("Theme", self.language_selection.get_understanding_language())
                ui.label(f"{theme_label}:").classes('font-medium text-gray-700')
                ui.label("Light").classes('text-gray-600')

            # Difficulty setting (placeholder)
            with ui.row().classes('w-full justify-between items-center mb-3'):
                difficulty_label = get_localized_string("Difficulty Level", self.language_selection.get_understanding_language())
                ui.label(f"{difficulty_label}:").classes('font-medium text-gray-700')
                ui.label("Intermediate").classes('text-gray-600')

            # Note about future features
            note_text = get_localized_string(
                "Additional settings will be available in future updates.",
                self.language_selection.get_understanding_language()
            )
            ui.label(note_text).classes('text-sm text-gray-500 italic')

    def render_about_section(self):
        """Render about section"""
        with ui.card().classes('p-4'):
            section_title = get_localized_string("About", self.language_selection.get_understanding_language())
            ui.label(section_title).classes('text-xl font-semibold mb-4 text-gray-800')

            # App info
            ui.label("Daily Sentence").classes('text-lg font-medium text-blue-600 mb-2')

            description = get_localized_string(
                "A language learning application that helps you practice sentence construction with guided constraints.",
                self.language_selection.get_understanding_language()
            )
            ui.label(description).classes('text-gray-600 mb-4 leading-relaxed')

            # Creator info
            with ui.row().classes('items-center'):
                created_by = get_localized_string("Created by", self.language_selection.get_understanding_language())
                ui.label(f"{created_by}:").classes('text-gray-600 mr-2')
                ui.link("Kevin Shiue", "https://buoren.net").classes('text-blue-600 hover:text-blue-800')

    def on_interface_language_change(self, new_language: str):
        """Handle interface language change"""
        self.language_selection.set_understanding_language(new_language)
        # Trigger a page refresh to update all text
        self.refresh()
