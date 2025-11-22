"""
Modern card component with shadows and elevation.
"""
import customtkinter as ctk
from typing import Optional


class ModernCard(ctk.CTkFrame):
    """
    Modern card component with elevation, shadows, and hover effects.
    Base component for all card-based UI elements.
    """
    
    def __init__(
        self,
        parent,
        corner_radius: int = 12,
        border_width: int = 0,
        border_color: Optional[str] = None,
        hover_effect: bool = False,
        **kwargs
    ):
        # Default colors with proper theme support
        fg_color = kwargs.pop('fg_color', ("white", "#1E1E1E"))
        
        super().__init__(
            parent,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=border_color or ("transparent", "transparent"),
            fg_color=fg_color,
            **kwargs
        )
        
        self.hover_effect = hover_effect
        self.original_fg = fg_color
        self.hover_fg = ("#F8F9FA", "#2A2A2A")
        
        if hover_effect:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Handle mouse enter for hover effect."""
        self.configure(fg_color=self.hover_fg)
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        self.configure(fg_color=self.original_fg)


class GradientProgress(ctk.CTkFrame):
    """
    Gradient progress bar with smooth animations.
    """
    
    def __init__(
        self,
        parent,
        progress: float = 0,
        gradient_colors: Optional[list] = None,
        height: int = 8,
        **kwargs
    ):
        super().__init__(
            parent,
            height=height,
            fg_color=("#E8EAED", "#353535"),
            corner_radius=height // 2,
            **kwargs
        )
        
        # Default gradient
        if gradient_colors is None:
            gradient_colors = ["#4A90E2", "#357ABD"]
        
        self.gradient_start = gradient_colors[0]
        self.gradient_end = gradient_colors[1] if len(gradient_colors) > 1 else gradient_colors[0]
        
        # Progress fill
        self.progress_fill = ctk.CTkFrame(
            self,
            fg_color=self.gradient_start,  # Use start color (gradient not natively supported)
            corner_radius=height // 2
        )
        
        self.set_progress(progress)
    
    def set_progress(self, progress: float):
        """Set progress percentage (0-100)."""
        progress = max(0, min(100, progress))
        if progress > 0:
            self.progress_fill.place(relx=0, rely=0, relwidth=progress/100, relheight=1)
        else:
            self.progress_fill.place_forget()
    
    def set_gradient(self, colors: list):
        """Update gradient colors."""
        self.gradient_start = colors[0]
        self.gradient_end = colors[1] if len(colors) > 1 else colors[0]
        self.progress_fill.configure(fg_color=self.gradient_start)


class TagChip(ctk.CTkFrame):
    """
    Tag/badge chip component with colored background.
    """
    
    def __init__(
        self,
        parent,
        text: str,
        color: str = "#4A90E2",
        text_color: str = "white",
        **kwargs
    ):
        super().__init__(
            parent,
            fg_color=color,
            corner_radius=12,
            **kwargs
        )
        
        # Text label
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=("Segoe UI", 11),
            text_color=text_color
        )
        self.label.pack(padx=10, pady=4)
    
    def set_text(self, text: str):
        """Update chip text."""
        self.label.configure(text=text)
    
    def set_color(self, color: str):
        """Update chip color."""
        self.configure(fg_color=color)


class MetricCard(ctk.CTkFrame):
    """
    Metric/stat card with gradient background and icon.
    """
    
    def __init__(
        self,
        parent,
        title: str,
        value: str,
        subtitle: str = "",
        icon: str = "📊",
        gradient_colors: Optional[list] = None,
        **kwargs
    ):
        # Default gradient
        if gradient_colors is None:
            gradient_colors = ["#4A90E2", "#357ABD"]
        
        super().__init__(
            parent,
            fg_color=gradient_colors[0],  # Use first gradient color
            corner_radius=12,
            **kwargs
        )
        
        # Content container
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=16)
        
        # Icon and title row
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        # Icon
        icon_label = ctk.CTkLabel(
            header,
            text=icon,
            font=("Segoe UI", 24)
        )
        icon_label.pack(side="left", padx=(0, 12))
        
        # Title
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 13),
            text_color="white",
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Value
        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=("Segoe UI", 32, "bold"),
            text_color="white",
            anchor="w"
        )
        value_label.pack(fill="x", pady=(8, 0))
        
        # Subtitle
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                content,
                text=subtitle,
                font=("Segoe UI", 11),
                text_color="rgba(255,255,255,0.8)",
                anchor="w"
            )
            subtitle_label.pack(fill="x", pady=(4, 0))
