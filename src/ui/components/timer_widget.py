"""
Timer widget component for time tracking.
"""
import customtkinter as ctk
from datetime import datetime
from typing import Callable, Optional


class TimerWidget(ctk.CTkFrame):
    """Timer widget for tracking time on tasks."""
    
    def __init__(self, parent, initial_seconds: int = 0, on_start: Optional[Callable] = None,
                 on_stop: Optional[Callable] = None, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        
        self.elapsed_seconds = initial_seconds
        self.running = False
        self.on_start_callback = on_start
        self.on_stop_callback = on_stop
        self.update_job = None
        
        self._create_ui()
        self._update_display()
    
    def _create_ui(self):
        """Create timer UI."""
        # Timer display
        self.time_label = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=("Segoe UI", 24, "bold"),
            text_color=("gray30", "gray80")
        )
        self.time_label.pack(pady=(12, 8))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=(0, 12))
        
        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶ Start",
            command=self._on_start,
            width=100,
            font=("Segoe UI", 12),
            fg_color=("#4CAF50", "#66BB6A"),
            hover_color=("#45A049", "#5CAA6A")
        )
        self.start_btn.pack(side="left", padx=4)
        
        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="⏸ Stop",
            command=self._on_stop,
            width=100,
            font=("Segoe UI", 12),
            fg_color=("#EF5350", "#E57373"),
            hover_color=("#E53935", "#EF5350"),
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=4)
        
        self.reset_btn = ctk.CTkButton(
            buttons_frame,
            text="↺ Reset",
            command=self._on_reset,
            width=100,
            font=("Segoe UI", 12),
            fg_color="gray60",
            hover_color="gray50"
        )
        self.reset_btn.pack(side="left", padx=4)
    
    def _update_display(self):
        """Update time display."""
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_label.configure(text=time_str)
        
        # Update background color when running
        if self.running:
            self.configure(fg_color=("#E8F5E9", "#2D4A2F"))
        else:
            self.configure(fg_color=("white", "#2D2D2D"))
    
    def _on_start(self):
        """Handle start button."""
        if not self.running:
            self.running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            
            # Call callback
            if self.on_start_callback:
                self.on_start_callback()
            
            # Start updating
            self._update_timer()
    
    def _on_stop(self):
        """Handle stop button."""
        if self.running:
            self.running = False
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            
            # Cancel update job
            if self.update_job:
                self.after_cancel(self.update_job)
                self.update_job = None
            
            # Call callback
            if self.on_stop_callback:
                self.on_stop_callback(self.elapsed_seconds)
            
            self._update_display()
    
    def _on_reset(self):
        """Handle reset button."""
        if not self.running:
            self.elapsed_seconds = 0
            self._update_display()
    
    def _update_timer(self):
        """Update timer every second."""
        if self.running:
            self.elapsed_seconds += 1
            self._update_display()
            # Schedule next update
            self.update_job = self.after(1000, self._update_timer)
    
    def get_elapsed_seconds(self) -> int:
        """Get total elapsed seconds."""
        return self.elapsed_seconds
    
    def is_running(self) -> bool:
        """Check if timer is running."""
        return self.running
    
    def stop_if_running(self):
        """Stop timer if it's running."""
        if self.running:
            self._on_stop()
