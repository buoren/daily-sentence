from nicegui import ui
from typing import List
from daily_sentence.language import LanguageSelection
from daily_sentence.pages.base_page import BasePage
from daily_sentence.pages.navigation import NavigationBar
from daily_sentence.pages.daily_practice_page import DailyPracticePage
from daily_sentence.pages.vocabulary_page import VocabularyPage
from daily_sentence.pages.settings_page import SettingsPage


class DailySentenceApp:
    """Main application controller that manages pages and navigation"""
    
    def __init__(self):
        self.language_selection = LanguageSelection("Dutch", "English")
        self.pages: List[BasePage] = []
        self.current_page_index = 0
        self.navigation_bar = None
        self.page_container = None
        
        # Initialize pages
        self.init_pages()
    
    def init_pages(self):
        """Initialize all application pages"""
        self.pages = [
            DailyPracticePage(self.language_selection),
            VocabularyPage(self.language_selection),
            SettingsPage(self.language_selection)
        ]
    
    def render(self):
        """Render the entire application"""
        # Set up the main layout
        with ui.column().classes('w-full min-h-screen bg-sky-100 p-4'):
            # Navigation bar
            self.navigation_bar = NavigationBar(
                self.pages, 
                self.language_selection, 
                self.on_page_change
            )
            self.navigation_bar.render()
            
            # Page container
            self.page_container = ui.element('div').classes('w-full flex justify-center')
            
            # Render initial page
            self.render_current_page()
    
    def render_current_page(self):
        """Render the currently selected page"""
        if self.page_container:
            self.page_container.clear()
            
            with self.page_container:
                current_page = self.pages[self.current_page_index]
                current_page.render()
    
    def on_page_change(self, page_index: int):
        """Handle page navigation"""
        if 0 <= page_index < len(self.pages):
            self.current_page_index = page_index
            self.render_current_page()
    
    def add_page(self, page: BasePage):
        """Add a new page to the application"""
        self.pages.append(page)
        if self.navigation_bar:
            self.navigation_bar.pages = self.pages
            self.navigation_bar.refresh()
    
    def get_current_page(self) -> BasePage:
        """Get the currently active page"""
        return self.pages[self.current_page_index]


def create_app() -> DailySentenceApp:
    """Factory function to create and configure the application"""
    app = DailySentenceApp()
    return app
