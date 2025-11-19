"""
Theme configuration and management for Desk Flow.
"""
import customtkinter as ctk
import darkdetect
from typing import Dict
from config import LIGHT_THEME, DARK_THEME


class ThemeManager:
    """Manages application themes and color schemes."""
    
    def __init__(self):
        self.current_mode = "light"  # light or dark
        self._init_customtkinter()
    
    def _init_customtkinter(self):
        """Initialize CustomTkinter with default theme."""
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")  # We'll override with custom colors
    
    def get_colors(self) -> Dict[str, str]:
        """Get current theme colors."""
        return LIGHT_THEME if self.current_mode == "light" else DARK_THEME
    
    def set_mode(self, mode: str):
        """Set theme mode: 'light', 'dark', or 'system'."""
        if mode == "system":
            # Detect system theme
            system_theme = darkdetect.theme()
            self.current_mode = "dark" if system_theme == "Dark" else "light"
        else:
            self.current_mode = mode
        
        # Apply to CustomTkinter
        ctk.set_appearance_mode(self.current_mode)
    
    def toggle_theme(self):
        """Toggle between light and dark modes."""
        self.current_mode = "dark" if self.current_mode == "light" else "light"
        ctk.set_appearance_mode(self.current_mode)
        return self.current_mode
    
    def get_mode(self) -> str:
        """Get current theme mode."""
        return self.current_mode


# Global theme manager instance
theme_manager = ThemeManager()
