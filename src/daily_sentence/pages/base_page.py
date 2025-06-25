from abc import ABC, abstractmethod
from nicegui import ui
from daily_sentence.language import LanguageSelection
from typing import Optional


class BasePage(ABC):
    """Abstract base class for all pages in the application"""
    
    def __init__(self, language_selection: LanguageSelection):
        self.language_selection = language_selection
        self.container: Optional[ui.element] = None
    
    @abstractmethod
    def get_title(self) -> str:
        """Return the page title for navigation"""
        pass
    
    @abstractmethod
    def get_icon(self) -> str:
        """Return the icon name for navigation tab"""
        pass
    
    @abstractmethod
    def render(self) -> ui.element:
        """Render the page content and return the container"""
        pass
    
    def on_language_changed(self):
        """Called when language selection changes - override if needed"""
        if self.container:
            self.refresh()
    
    def refresh(self):
        """Refresh the page content"""
        if self.container:
            self.container.clear()
            with self.container:
                self.render_content()
    
    @abstractmethod
    def render_content(self):
        """Render the actual page content - called by render() and refresh()"""
        pass
