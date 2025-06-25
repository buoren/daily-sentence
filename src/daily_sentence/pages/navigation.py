from nicegui import ui
from typing import List, Callable
from daily_sentence.pages.base_page import BasePage
from daily_sentence.language import LanguageSelection
from daily_sentence.chatgpt_utils import get_localized_string


class NavigationBar:
    """Navigation bar component with tabs"""
    
    def __init__(self, pages: List[BasePage], language_selection: LanguageSelection, on_page_change: Callable[[int], None]):
        self.pages = pages
        self.language_selection = language_selection
        self.on_page_change = on_page_change
        self.current_page_index = 0
        self.nav_container = None
        self.language_dropdown = None
    
    def render(self) -> ui.element:
        """Render the navigation bar"""
        self.nav_container = ui.card().classes('w-full mb-4 p-2 bg-white shadow-sm')
        with self.nav_container:
            with ui.row().classes('w-full justify-between items-center'):
                # Language selection on the left
                self.render_language_selector()
                
                # Page tabs in the center
                self.render_page_tabs()
                
                # Logo/branding on the right
                with ui.row().classes('items-center'):
                    ui.label("Daily Sentence").classes('text-lg font-semibold text-gray-700')
        
        return self.nav_container
    
    def render_language_selector(self):
        """Render the language selection dropdowns"""
        with ui.row().classes('items-center space-x-2'):
            # Understanding language dropdown
            understanding_lang = self.language_selection.get_understanding_language()
            learning_lang = self.language_selection.get_learning_language()
            
            from daily_sentence.language import get_supported_languages
            languages = get_supported_languages()
            
            # I understand dropdown
            understand_label = get_localized_string("I understand", understanding_lang)
            with ui.dropdown_button(f"{understand_label}: {understanding_lang}", auto_close=True).classes('text-sm'):
                for lang in languages:
                    def make_understand_handler(language=lang):
                        def handler():
                            self.language_selection.set_understanding_language(language)
                            self.on_language_change()
                        return handler
                    
                    ui.item(f"{understand_label}: {lang}", on_click=make_understand_handler())
            
            # Learning language dropdown  
            learn_label = get_localized_string("Learning", understanding_lang)
            with ui.dropdown_button(f"{learn_label}: {learning_lang}", auto_close=True).classes('text-sm'):
                for lang in languages:
                    def make_learn_handler(language=lang):
                        def handler():
                            self.language_selection.set_learning_language(language)
                            self.on_language_change()
                        return handler
                    
                    ui.item(f"{learn_label}: {lang}", on_click=make_learn_handler())
    
    def render_page_tabs(self):
        """Render the page navigation tabs"""
        with ui.row().classes('space-x-1'):
            for i, page in enumerate(self.pages):
                is_active = i == self.current_page_index
                tab_classes = 'px-4 py-2 rounded-lg transition-all duration-200'
                if is_active:
                    tab_classes += ' bg-blue-500 text-white shadow-md'
                else:
                    tab_classes += ' bg-gray-100 text-gray-700 hover:bg-gray-200'
                
                title = get_localized_string(page.get_title(), self.language_selection.get_understanding_language())
                
                def make_tab_handler(page_index=i):
                    def handler():
                        self.switch_to_page(page_index)
                    return handler
                
                with ui.button(on_click=make_tab_handler()).classes(tab_classes):
                    if page.get_icon():
                        ui.icon(page.get_icon()).classes('mr-2')
                    ui.label(title)
    
    def switch_to_page(self, page_index: int):
        """Switch to a specific page"""
        if 0 <= page_index < len(self.pages):
            self.current_page_index = page_index
            self.refresh_tabs()
            self.on_page_change(page_index)
    
    def on_language_change(self):
        """Called when language selection changes"""
        self.refresh()
        # Notify all pages about language change
        for page in self.pages:
            page.on_language_changed()
    
    def refresh(self):
        """Refresh the navigation bar"""
        if self.nav_container:
            self.nav_container.clear()
            with self.nav_container:
                with ui.row().classes('w-full justify-between items-center'):
                    self.render_language_selector()
                    self.render_page_tabs()
                    with ui.row().classes('items-center'):
                        ui.label("Daily Sentence").classes('text-lg font-semibold text-gray-700')
    
    def refresh_tabs(self):
        """Refresh only the tabs (for performance)"""
        if self.nav_container:
            # This is a simple approach - in a more complex app you might want to update individual tab styles
            self.refresh()
