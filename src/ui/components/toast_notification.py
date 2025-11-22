"""
Toast notification widget for non-intrusive notifications.
"""
import customtkinter as ctk
from typing import Callable, Optional
import time


class ToastNotification(ctk.CTkToplevel):
    """Toast notification that appears in bottom-right corner."""
    
    # Class variable to track active toasts
    active_toasts = []
    toast_offset = 20  # Pixels from bottom
    toast_spacing = 90  # Spacing between toasts
    
    def __init__(self, parent, title: str, message: str, 
                 duration: int = 5000, on_click: Optional[Callable] = None):
        super().__init__(parent)
        
        self.title_text = title
        self.message_text = message
        self.duration = duration
        self.on_click_callback = on_click
        
        # Configure window
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Always on top
        self.geometry("350x80")
        
        # Calculate position (bottom-right, stacked if multiple)
        self._calculate_position()
        
        # Create UI
        self._create_ui()
        
        # Auto-dismiss after duration
        if self.duration > 0:
            self.after(self.duration, self._dismiss)
        
        # Add to active toasts
        ToastNotification.active_toasts.append(self)
        
        # Slide in animation (simple version)
        self._slide_in()
    
    def _calculate_position(self):
        """Calculate position based on screen and existing toasts."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Count existing toasts to stack vertically
        y_offset = ToastNotification.toast_offset + (
            len(ToastNotification.active_toasts) * ToastNotification.toast_spacing
        )
        
        x = screen_width - 370  # 350 width + 20 margin
        y = screen_height - y_offset - 80  # 80 is toast height
        
        self.geometry(f"+{x}+{y}")
    
    def _create_ui(self):
        """Create toast UI."""
        # Main container with shadow effect
        container = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=("#FFFFFF", "#2A2A2A"),
            border_width=1,
            border_color=("#DADCE0", "#3C4043")
        )
        container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Make clickable
        if self.on_click_callback:
            container.bind("<Button-1>", lambda e: self._on_click())
            self.configure(cursor="hand2")
        
        # Content frame
        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Header with icon and close button
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 4))
        
        # Icon and title
        icon_title_frame = ctk.CTkFrame(header, fg_color="transparent")
        icon_title_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            icon_title_frame,
            text=self._get_icon(),
            font=("Segoe UI", 16)
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            icon_title_frame,
            text=self.title_text,
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        # Close button
        close_btn = ctk.CTkButton(
            header,
            text="✕",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color=("#E8EAED", "#353535"),
            text_color=("gray60", "gray80"),
            command=self._dismiss,
            font=("Segoe UI", 14)
        )
        close_btn.pack(side="right")
        
        # Message
        ctk.CTkLabel(
            content,
            text=self.message_text,
            font=("Segoe UI", 11),
            text_color=("#5F6368", "#9AA0A6"),
            anchor="w",
            justify="left",
            wraplength=310
        ).pack(fill="x")
    
    def _get_icon(self) -> str:
        """Get icon based on notification type."""
        if "due" in self.title_text.lower() or "overdue" in self.title_text.lower():
            return "⏰"
        elif "complete" in self.title_text.lower():
            return "✅"
        elif "timer" in self.title_text.lower():
            return "⏱️"
        elif "summary" in self.title_text.lower():
            return "📋"
        else:
            return "🔔"
    
    def _slide_in(self):
        """Simple slide-in animation."""
        # Could implement slide animation here
        # For now, just show immediately
        pass
    
    def _on_click(self):
        """Handle toast click."""
        if self.on_click_callback:
            self.on_click_callback()
            self._dismiss()
    
    def _dismiss(self):
        """Dismiss the toast."""
        # Remove from active toasts
        if self in ToastNotification.active_toasts:
            ToastNotification.active_toasts.remove(self)
        
        # Reposition remaining toasts
        self._reposition_toasts()
        
        # Destroy window
        self.destroy()
    
    @staticmethod
    def _reposition_toasts():
        """Reposition all active toasts after one is dismissed."""
        for i, toast in enumerate(ToastNotification.active_toasts):
            screen_width = toast.winfo_screenwidth()
            screen_height = toast.winfo_screenheight()
            
            y_offset = ToastNotification.toast_offset + (i * ToastNotification.toast_spacing)
            x = screen_width - 370
            y = screen_height - y_offset - 80
            
            toast.geometry(f"+{x}+{y}")
    
    @staticmethod
    def show(parent, title: str, message: str, duration: int = 5000, 
             on_click: Optional[Callable] = None):
        """Static method to show a toast notification."""
        return ToastNotification(parent, title, message, duration, on_click)
