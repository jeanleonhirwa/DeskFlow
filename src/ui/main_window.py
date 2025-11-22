"""
Main application window.
"""
import customtkinter as ctk
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    APP_NAME, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
)
from data.storage import StorageManager
from ui.theme import theme_manager
from ui.components.navigation import NavigationBar
from ui.components.settings_dialog import SettingsDialog
from ui.views.projects import ProjectsView
from ui.views.tasks import TasksView
from ui.views.daily_planner import DailyPlannerView
from ui.views.analytics import AnalyticsView


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize storage
        self.storage = StorageManager()
        
        # Load settings
        self.settings = self.storage.get_settings()
        
        # Configure window
        self.title(APP_NAME)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Set theme from settings
        theme_manager.set_mode(self.settings.theme)
        
        # Initialize UI
        self._create_ui()
        
        # Setup keyboard shortcuts
        self._setup_keyboard_shortcuts()
        
        # Load initial view
        self._show_view("projects")
        
        # Save window state on close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_ui(self):
        """Create main UI structure."""
        # Navigation bar
        self.nav_bar = NavigationBar(
            self,
            on_tab_change=self._on_tab_change,
            on_theme_toggle=self._on_theme_toggle,
            on_settings=self._on_settings
        )
        self.nav_bar.pack(fill="x", side="top")
        
        # Main content area
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True)
        
        # Create views (but don't show them yet)
        self.views = {}
        self.current_view = None
    
    def _get_or_create_view(self, view_name: str):
        """Get existing view or create new one."""
        if view_name not in self.views:
            if view_name == "projects":
                self.views[view_name] = ProjectsView(self.content_area, self.storage)
            elif view_name == "tasks":
                self.views[view_name] = TasksView(self.content_area, self.storage)
            elif view_name == "daily_planner":
                self.views[view_name] = DailyPlannerView(self.content_area, self.storage)
            elif view_name == "analytics":
                self.views[view_name] = AnalyticsView(self.content_area, self.storage)
        
        return self.views[view_name]
    
    def _show_view(self, view_name: str):
        """Show the specified view."""
        # Hide current view
        if self.current_view:
            self.current_view.pack_forget()
        
        # Get or create and show new view
        view = self._get_or_create_view(view_name)
        view.pack(fill="both", expand=True)
        
        # Refresh data if view has refresh method
        if hasattr(view, 'refresh'):
            view.refresh()
        
        self.current_view = view
    
    def _on_tab_change(self, tab_id: str):
        """Handle navigation tab change."""
        self._show_view(tab_id)
    
    def _on_theme_toggle(self) -> str:
        """Handle theme toggle."""
        mode = theme_manager.toggle_theme()
        
        # Save theme preference
        self.settings.update(theme=mode)
        self.storage.save_settings(self.settings)
        
        # Update nav bar icon
        self.nav_bar.set_theme_icon(mode)
        
        return mode
    
    def _on_theme_change(self, theme: str):
        """Handle theme change from settings."""
        theme_manager.set_mode(theme)
        
        # Update nav bar icon
        mode = theme_manager.get_mode()
        self.nav_bar.set_theme_icon(mode)
    
    def _on_settings(self):
        """Handle settings button click."""
        dialog = SettingsDialog(self, self.storage, self._on_theme_change)
        dialog.wait_window()
        
        # Reload settings after dialog closes
        self.settings = self.storage.get_settings()
    
    def _setup_keyboard_shortcuts(self):
        """Setup global keyboard shortcuts."""
        # Navigation shortcuts - Ctrl+1-4
        self.bind("<Control-Key-1>", lambda e: self._quick_nav("projects"))
        self.bind("<Control-Key-2>", lambda e: self._quick_nav("tasks"))
        self.bind("<Control-Key-3>", lambda e: self._quick_nav("daily_planner"))
        self.bind("<Control-Key-4>", lambda e: self._quick_nav("analytics"))
        
        # Action shortcuts
        self.bind("<Control-n>", lambda e: self._quick_new())
        self.bind("<Control-f>", lambda e: self._quick_search())
        
        # Utility shortcuts
        self.bind("<Control-comma>", lambda e: self._on_settings())  # Ctrl+,
        self.bind("<Control-t>", lambda e: self._on_theme_toggle())
        self.bind("<Control-q>", lambda e: self._on_closing())
    
    def _quick_nav(self, view_name: str):
        """Quick navigation to view via keyboard."""
        self.nav_bar.set_active_tab(view_name)
        self._show_view(view_name)
    
    def _quick_new(self):
        """Create new item based on current view."""
        if self.current_view:
            view_class = self.current_view.__class__.__name__
            if view_class == "ProjectsView":
                self.current_view._on_create_project()
            elif view_class == "TasksView":
                self.current_view._on_create_task()
            # Daily Planner doesn't have a "new" action
    
    def _quick_search(self):
        """Focus search bar in current view."""
        if self.current_view and hasattr(self.current_view, 'search_bar'):
            self.current_view.search_bar.focus_set()
    
    def _on_closing(self):
        """Handle window close event."""
        # Save window size and position
        self.settings.update(
            window_size={
                "width": self.winfo_width(),
                "height": self.winfo_height()
            },
            window_position={
                "x": self.winfo_x(),
                "y": self.winfo_y()
            }
        )
        self.storage.save_settings(self.settings)
        
        # Close application
        self.destroy()
    
    def run(self):
        """Run the application."""
        self.mainloop()
