"""
Common reusable UI components.
"""
import customtkinter as ctk
from typing import Callable, Optional


class StatusBadge(ctk.CTkFrame):
    """Status badge component with colored background."""
    
    def __init__(self, parent, text: str, color: str, **kwargs):
        super().__init__(parent, fg_color=color, corner_radius=6, **kwargs)
        
        self.label = ctk.CTkLabel(
            self,
            text=text.upper(),
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        )
        self.label.pack(padx=8, pady=4)


class PriorityIndicator(ctk.CTkFrame):
    """Priority indicator dot."""
    
    COLORS = {
        "low": "#4CAF50",
        "medium": "#FFA726",
        "high": "#EF5350"
    }
    
    def __init__(self, parent, priority: str, **kwargs):
        color = self.COLORS.get(priority, "#999999")
        super().__init__(parent, fg_color=color, corner_radius=4, width=8, height=8, **kwargs)


class ProgressBar(ctk.CTkFrame):
    """Custom progress bar component."""
    
    def __init__(self, parent, progress: float, color: str = "#E07B53", **kwargs):
        super().__init__(parent, fg_color="#E0E0E0", corner_radius=8, height=8, **kwargs)
        
        self.progress_fill = ctk.CTkFrame(
            self,
            fg_color=color,
            corner_radius=8,
            height=8
        )
        self.set_progress(progress)
    
    def set_progress(self, progress: float):
        """Set progress percentage (0-100)."""
        progress = max(0, min(100, progress))
        if progress > 0:
            self.progress_fill.place(relx=0, rely=0, relwidth=progress/100, relheight=1)
        else:
            self.progress_fill.place_forget()


class IconButton(ctk.CTkButton):
    """Icon button with optional text."""
    
    def __init__(self, parent, text: str = "", command: Optional[Callable] = None, **kwargs):
        defaults = {
            "corner_radius": 8,
            "font": ("Segoe UI", 13),
            "height": 36
        }
        defaults.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **defaults)


class SearchBar(ctk.CTkFrame):
    """Search bar with icon and clear button."""
    
    def __init__(self, parent, placeholder: str = "Search...", on_change: Optional[Callable] = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.on_change = on_change
        
        # Search icon (using text)
        self.icon = ctk.CTkLabel(self, text="🔍", font=("Segoe UI", 14))
        self.icon.pack(side="left", padx=(0, 8))
        
        # Search entry
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            border_width=0,
            font=("Segoe UI", 13)
        )
        self.entry.pack(side="left", fill="x", expand=True)
        
        # Bind change event
        if on_change:
            self.entry.bind("<KeyRelease>", lambda e: on_change(self.entry.get()))
    
    def get(self) -> str:
        """Get search text."""
        return self.entry.get()
    
    def clear(self):
        """Clear search text."""
        self.entry.delete(0, "end")


class EmptyState(ctk.CTkFrame):
    """Empty state component with message and optional action."""
    
    def __init__(self, parent, message: str, action_text: Optional[str] = None, 
                 action_command: Optional[Callable] = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Center content
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Empty state icon (using emoji)
        icon = ctk.CTkLabel(content, text="📭", font=("Segoe UI", 48))
        icon.pack(pady=(0, 16))
        
        # Message
        label = ctk.CTkLabel(
            content,
            text=message,
            font=("Segoe UI", 14),
            text_color="gray"
        )
        label.pack()
        
        # Optional action button
        if action_text and action_command:
            button = IconButton(
                content,
                text=action_text,
                command=action_command
            )
            button.pack(pady=(16, 0))
