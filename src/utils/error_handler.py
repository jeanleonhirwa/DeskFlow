"""
Centralized error handling and logging.
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
import customtkinter as ctk


# Setup logging
def setup_logging():
    """Setup error logging to file."""
    from config import LOGS_DIR
    
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create log file
    log_file = LOGS_DIR / "error.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    return logging.getLogger(__name__)


# Initialize logger
logger = setup_logging()


class ErrorHandler:
    """Centralized error handling for the application."""
    
    @staticmethod
    def handle_storage_error(exception: Exception, context: str = "Storage operation"):
        """Handle storage and file I/O errors."""
        error_msg = f"{context} failed: {str(exception)}"
        logger.error(error_msg, exc_info=True)
        
        ErrorHandler.show_error_dialog(
            "Storage Error",
            f"An error occurred while accessing data:\n\n{str(exception)}\n\nPlease check if you have write permissions and sufficient disk space."
        )
    
    @staticmethod
    def handle_validation_error(message: str, field_name: Optional[str] = None):
        """Handle data validation errors."""
        if field_name:
            full_message = f"Invalid {field_name}: {message}"
        else:
            full_message = message
        
        logger.warning(f"Validation error: {full_message}")
        
        ErrorHandler.show_warning_dialog(
            "Validation Error",
            full_message
        )
    
    @staticmethod
    def handle_parsing_error(exception: Exception, data_type: str = "data"):
        """Handle JSON/date parsing errors."""
        error_msg = f"Failed to parse {data_type}: {str(exception)}"
        logger.error(error_msg, exc_info=True)
        
        ErrorHandler.show_error_dialog(
            "Parse Error",
            f"Could not parse {data_type}. The data may be corrupted.\n\nError: {str(exception)}"
        )
    
    @staticmethod
    def handle_unexpected_error(exception: Exception, context: str = "Operation"):
        """Handle unexpected/unknown errors."""
        error_msg = f"Unexpected error during {context}: {str(exception)}"
        logger.error(error_msg, exc_info=True)
        
        ErrorHandler.show_error_dialog(
            "Unexpected Error",
            f"An unexpected error occurred:\n\n{str(exception)}\n\nThe error has been logged. Please restart the application."
        )
    
    @staticmethod
    def show_error_dialog(title: str, message: str, parent=None):
        """Display error dialog to user."""
        dialog = ctk.CTkToplevel(parent) if parent else ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("450x200")
        dialog.resizable(False, False)
        
        # Make modal if parent exists
        if parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        # Icon and message
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="❌ " + title,
            font=("Segoe UI", 14, "bold"),
            text_color="red"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            content_frame,
            text=message,
            font=("Segoe UI", 12),
            wraplength=400,
            justify="left"
        ).pack(pady=(0, 20))
        
        ctk.CTkButton(
            content_frame,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
    
    @staticmethod
    def show_warning_dialog(title: str, message: str, parent=None):
        """Display warning dialog to user."""
        dialog = ctk.CTkToplevel(parent) if parent else ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("450x180")
        dialog.resizable(False, False)
        
        if parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="⚠️ " + title,
            font=("Segoe UI", 14, "bold"),
            text_color="orange"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            content_frame,
            text=message,
            font=("Segoe UI", 12),
            wraplength=400,
            justify="left"
        ).pack(pady=(0, 20))
        
        ctk.CTkButton(
            content_frame,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
    
    @staticmethod
    def show_success_message(message: str, parent=None):
        """Show success notification."""
        dialog = ctk.CTkToplevel(parent) if parent else ctk.CTkToplevel()
        dialog.title("Success")
        dialog.geometry("350x120")
        dialog.resizable(False, False)
        
        if parent:
            dialog.transient(parent)
        
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="✓ " + message,
            font=("Segoe UI", 13),
            text_color=("#4CAF50", "#66BB6A")
        ).pack(pady=(10, 20))
        
        ctk.CTkButton(
            content_frame,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack()
        
        # Center and auto-close after 2 seconds
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        dialog.after(2000, dialog.destroy)
