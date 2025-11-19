"""
Top navigation bar component.
"""
import customtkinter as ctk
from typing import Callable, Optional


class NavigationBar(ctk.CTkFrame):
    """Top navigation bar with tabs and theme toggle."""
    
    def __init__(self, parent, on_tab_change: Callable, on_theme_toggle: Callable, 
                 on_settings: Callable, **kwargs):
        super().__init__(parent, fg_color="transparent", height=60, **kwargs)
        
        self.on_tab_change = on_tab_change
        self.on_theme_toggle = on_theme_toggle
        self.on_settings = on_settings
        
        self.current_tab = "projects"
        self.tab_buttons = {}
        
        self._create_ui()
    
    def _create_ui(self):
        """Create navigation UI."""
        # Left side - App name and tabs
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        # App name/logo
        app_name = ctk.CTkLabel(
            left_frame,
            text="⚡ Desk Flow",
            font=("Segoe UI", 18, "bold")
        )
        app_name.pack(side="left", padx=(0, 40))
        
        # Navigation tabs
        tabs_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        tabs_frame.pack(side="left", fill="y")
        
        tabs = [
            ("projects", "Projects"),
            ("tasks", "Tasks"),
            ("daily_planner", "Daily Planner"),
            ("analytics", "Analytics")
        ]
        
        for tab_id, tab_name in tabs:
            btn = ctk.CTkButton(
                tabs_frame,
                text=tab_name,
                command=lambda tid=tab_id: self._on_tab_click(tid),
                fg_color="transparent",
                text_color="gray60",
                hover_color=("gray85", "gray25"),
                font=("Segoe UI", 13),
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", padx=4)
            self.tab_buttons[tab_id] = btn
        
        # Set initial active tab
        self._set_active_tab("projects")
        
        # Right side - Theme toggle and settings
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=10)
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            right_frame,
            text="🌙",
            command=self._on_theme_toggle_click,
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=("Segoe UI", 18)
        )
        self.theme_btn.pack(side="left", padx=4)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            right_frame,
            text="⚙️",
            command=on_settings,
            width=40,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=("Segoe UI", 18)
        )
        settings_btn.pack(side="left", padx=4)
    
    def _on_tab_click(self, tab_id: str):
        """Handle tab click."""
        self._set_active_tab(tab_id)
        self.on_tab_change(tab_id)
    
    def _set_active_tab(self, tab_id: str):
        """Set the active tab visual state."""
        self.current_tab = tab_id
        
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.configure(
                    fg_color=("#E07B53", "#F4A261"),
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="gray60"
                )
    
    def _on_theme_toggle_click(self):
        """Handle theme toggle click."""
        mode = self.on_theme_toggle()
        # Update icon based on mode
        self.theme_btn.configure(text="☀️" if mode == "dark" else "🌙")
    
    def set_theme_icon(self, mode: str):
        """Set theme icon based on mode."""
        self.theme_btn.configure(text="☀️" if mode == "dark" else "🌙")
