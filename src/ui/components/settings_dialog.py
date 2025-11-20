"""
Settings dialog component.
"""
import customtkinter as ctk
from typing import Callable
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from models.settings import Settings
from data.storage import StorageManager
from ui.components.common import IconButton
from config import PROJECT_COLORS


class SettingsDialog(ctk.CTkToplevel):
    """Settings configuration dialog."""
    
    def __init__(self, parent, storage: StorageManager, on_theme_change: Callable):
        super().__init__(parent)
        
        self.storage = storage
        self.on_theme_change = on_theme_change
        self.settings = storage.get_settings()
        
        # Configure window
        self.title("Settings")
        self.geometry("700x600")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        """Create settings UI with tabs."""
        # Tab view
        self.tabview = ctk.CTkTabview(self, width=660, height=480)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Appearance")
        self.tabview.add("General")
        self.tabview.add("Data & Backup")
        self.tabview.add("About")
        
        self._create_appearance_tab()
        self._create_general_tab()
        self._create_backup_tab()
        self._create_about_tab()
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = IconButton(
            buttons_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="gray70",
            hover_color="gray60"
        )
        cancel_btn.pack(side="right", padx=(8, 0))
        
        save_btn = IconButton(
            buttons_frame,
            text="Save Settings",
            command=self._on_save,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white",
            font=("Segoe UI", 13, "bold")
        )
        save_btn.pack(side="right")
    
    def _create_appearance_tab(self):
        """Create appearance settings tab."""
        tab = self.tabview.tab("Appearance")
        
        # Theme selection
        ctk.CTkLabel(tab, text="Theme", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 8))
        
        theme_frame = ctk.CTkFrame(tab, fg_color="transparent")
        theme_frame.pack(fill="x", pady=(0, 20))
        
        self.theme_var = ctk.StringVar(value=self.settings.theme)
        
        themes = [
            ("light", "☀️ Light"),
            ("dark", "🌙 Dark"),
            ("system", "💻 System")
        ]
        
        for value, label in themes:
            radio = ctk.CTkRadioButton(
                theme_frame,
                text=label,
                variable=self.theme_var,
                value=value,
                font=("Segoe UI", 13),
                command=self._on_theme_preview
            )
            radio.pack(anchor="w", pady=4)
        
        # Font size (placeholder for future)
        ctk.CTkLabel(tab, text="Font Size", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        ctk.CTkLabel(
            tab,
            text="Font size adjustment coming soon...",
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack(anchor="w")
    
    def _create_general_tab(self):
        """Create general settings tab."""
        tab = self.tabview.tab("General")
        
        # Default project color
        ctk.CTkLabel(tab, text="Default Project Color", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 8))
        
        colors_frame = ctk.CTkFrame(tab, fg_color="transparent")
        colors_frame.pack(fill="x", pady=(0, 20))
        
        self.selected_color = self.settings.default_project_color
        
        for color in PROJECT_COLORS[:5]:  # Show first 5 colors
            btn = ctk.CTkButton(
                colors_frame,
                text="",
                width=40,
                height=40,
                corner_radius=20,
                fg_color=color,
                hover_color=color,
                border_width=2 if color == self.selected_color else 0,
                border_color=("#E07B53", "#F4A261"),
                command=lambda c=color: self._select_color(c)
            )
            btn.pack(side="left", padx=4)
        
        # Work hours
        ctk.CTkLabel(tab, text="Work Hours", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        
        hours_frame = ctk.CTkFrame(tab, fg_color="transparent")
        hours_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(hours_frame, text="Start:", font=("Segoe UI", 13)).pack(side="left", padx=(0, 8))
        self.work_start_entry = ctk.CTkEntry(hours_frame, width=100, font=("Segoe UI", 13))
        self.work_start_entry.insert(0, self.settings.work_hours_start)
        self.work_start_entry.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(hours_frame, text="End:", font=("Segoe UI", 13)).pack(side="left", padx=(0, 8))
        self.work_end_entry = ctk.CTkEntry(hours_frame, width=100, font=("Segoe UI", 13))
        self.work_end_entry.insert(0, self.settings.work_hours_end)
        self.work_end_entry.pack(side="left")
        
        ctk.CTkLabel(
            tab,
            text="Format: HH:MM (24-hour)",
            font=("Segoe UI", 11),
            text_color="gray60"
        ).pack(anchor="w")
    
    def _create_backup_tab(self):
        """Create backup settings tab."""
        tab = self.tabview.tab("Data & Backup")
        
        # Auto-backup toggle
        ctk.CTkLabel(tab, text="Automatic Backups", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 8))
        
        self.auto_backup_var = ctk.BooleanVar(value=self.settings.auto_backup)
        backup_toggle = ctk.CTkSwitch(
            tab,
            text="Enable automatic backups",
            variable=self.auto_backup_var,
            font=("Segoe UI", 13)
        )
        backup_toggle.pack(anchor="w", pady=(0, 20))
        
        # Manual backup button
        ctk.CTkLabel(tab, text="Manual Backup", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        
        manual_frame = ctk.CTkFrame(tab, fg_color="transparent")
        manual_frame.pack(fill="x", pady=(0, 20))
        
        backup_btn = IconButton(
            manual_frame,
            text="Create Backup Now",
            command=self._create_manual_backup,
            fg_color=("#4CAF50", "#66BB6A"),
            hover_color=("#45A049", "#5CAA6A")
        )
        backup_btn.pack(side="left")
        
        self.backup_status = ctk.CTkLabel(
            manual_frame,
            text="",
            font=("Segoe UI", 12),
            text_color="gray60"
        )
        self.backup_status.pack(side="left", padx=(16, 0))
        
        # Export/Import section
        ctk.CTkLabel(tab, text="Export Data", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        
        export_frame = ctk.CTkFrame(tab, fg_color="transparent")
        export_frame.pack(fill="x", pady=(0, 8))
        
        IconButton(
            export_frame,
            text="📤 Export All (JSON)",
            command=self._export_all_json,
            width=180,
            font=("Segoe UI", 12)
        ).pack(side="left", padx=(0, 8))
        
        IconButton(
            export_frame,
            text="📊 Export Projects (CSV)",
            command=self._export_projects_csv,
            width=180,
            font=("Segoe UI", 12)
        ).pack(side="left", padx=(0, 8))
        
        IconButton(
            export_frame,
            text="📋 Export Tasks (CSV)",
            command=self._export_tasks_csv,
            width=180,
            font=("Segoe UI", 12)
        ).pack(side="left")
        
        # Import section
        ctk.CTkLabel(tab, text="Import Data", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(12, 8))
        
        import_frame = ctk.CTkFrame(tab, fg_color="transparent")
        import_frame.pack(fill="x", pady=(0, 20))
        
        IconButton(
            import_frame,
            text="📥 Import from JSON",
            command=self._import_json,
            width=180,
            font=("Segoe UI", 12)
        ).pack(side="left")
        
        self.import_status = ctk.CTkLabel(
            import_frame,
            text="",
            font=("Segoe UI", 12),
            text_color="gray60"
        )
        self.import_status.pack(side="left", padx=(16, 0))
        
        # Data location
        ctk.CTkLabel(tab, text="Data Storage", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        
        from config import APP_DATA_DIR
        location_text = f"Location: {APP_DATA_DIR}"
        ctk.CTkLabel(
            tab,
            text=location_text,
            font=("Segoe UI", 11),
            text_color="gray60"
        ).pack(anchor="w")
        
        # Clear all data (dangerous)
        ctk.CTkLabel(tab, text="Danger Zone", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        
        clear_btn = IconButton(
            tab,
            text="Clear All Data",
            command=self._confirm_clear_data,
            fg_color="red",
            hover_color="darkred",
            text_color="white"
        )
        clear_btn.pack(anchor="w")
    
    def _create_about_tab(self):
        """Create about tab."""
        tab = self.tabview.tab("About")
        
        # Center content
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.place(relx=0.5, rely=0.4, anchor="center")
        
        # App icon/name
        ctk.CTkLabel(
            content,
            text="⚡ Desk Flow",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(0, 8))
        
        # Version
        from config import APP_VERSION
        ctk.CTkLabel(
            content,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 14),
            text_color="gray60"
        ).pack(pady=(0, 20))
        
        # Description
        ctk.CTkLabel(
            content,
            text="A clean, offline-first project management\napplication for software developers",
            font=("Segoe UI", 13),
            text_color="gray60",
            justify="center"
        ).pack(pady=(0, 20))
        
        # Credits
        ctk.CTkLabel(
            content,
            text="Built with Python & CustomTkinter",
            font=("Segoe UI", 12),
            text_color="gray50"
        ).pack()
    
    def _on_theme_preview(self):
        """Preview theme change."""
        theme = self.theme_var.get()
        self.on_theme_change(theme)
    
    def _select_color(self, color: str):
        """Select default project color."""
        self.selected_color = color
        # Update button borders
        for child in self.tabview.tab("General").winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for btn in child.winfo_children():
                    if isinstance(btn, ctk.CTkButton) and btn.cget("width") == 40:
                        btn_color = btn.cget("fg_color")
                        if isinstance(btn_color, tuple):
                            btn_color = btn_color[0]
                        if btn_color == color:
                            btn.configure(border_width=2)
                        else:
                            btn.configure(border_width=0)
    
    def _create_manual_backup(self):
        """Create manual backup."""
        from datetime import datetime
        from config import PROJECTS_FILE, TASKS_FILE, DAILY_PLANS_FILE, SETTINGS_FILE
        
        # Create backups
        for file in [PROJECTS_FILE, TASKS_FILE, DAILY_PLANS_FILE, SETTINGS_FILE]:
            if file.exists():
                self.storage._create_backup(file)
        
        # Show success message
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.backup_status.configure(text=f"✓ Backup created at {timestamp}")
    
    def _confirm_clear_data(self):
        """Confirm before clearing all data."""
        dialog = ctk.CTkInputDialog(
            text="Type 'DELETE' to confirm clearing all data:",
            title="Clear All Data"
        )
        result = dialog.get_input()
        
        if result == "DELETE":
            self._clear_all_data()
    
    def _clear_all_data(self):
        """Clear all application data."""
        from config import PROJECTS_FILE, TASKS_FILE, DAILY_PLANS_FILE
        
        # Create backup first
        self._create_manual_backup()
        
        # Clear data files
        self.storage._write_json(PROJECTS_FILE, [])
        self.storage._write_json(TASKS_FILE, [])
        self.storage._write_json(DAILY_PLANS_FILE, [])
        
        # Show success and close
        self.backup_status.configure(text="✓ All data cleared (backup created)")
        self.after(2000, self.destroy)
    
    def _export_all_json(self):
        """Export all data to JSON."""
        from tkinter import filedialog
        from utils.export_utils import export_all_data_json
        from datetime import datetime
        
        filename = f"deskflow_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=filename
        )
        
        if filepath:
            success = export_all_data_json(self.storage, filepath)
            if success:
                self.backup_status.configure(text="✓ Data exported successfully")
            else:
                self.backup_status.configure(text="✗ Export failed")
    
    def _export_projects_csv(self):
        """Export projects to CSV."""
        from tkinter import filedialog
        from utils.export_utils import export_projects_csv
        from datetime import datetime
        
        filename = f"projects_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename
        )
        
        if filepath:
            projects = self.storage.get_all_projects()
            success = export_projects_csv(projects, filepath)
            if success:
                self.backup_status.configure(text="✓ Projects exported")
            else:
                self.backup_status.configure(text="✗ Export failed")
    
    def _export_tasks_csv(self):
        """Export tasks to CSV."""
        from tkinter import filedialog
        from utils.export_utils import export_tasks_csv
        from datetime import datetime
        
        filename = f"tasks_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename
        )
        
        if filepath:
            tasks = self.storage.get_all_tasks()
            success = export_tasks_csv(tasks, filepath)
            if success:
                self.backup_status.configure(text="✓ Tasks exported")
            else:
                self.backup_status.configure(text="✗ Export failed")
    
    def _import_json(self):
        """Import data from JSON."""
        from tkinter import filedialog
        from utils.export_utils import import_all_data_json
        
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Select JSON file to import"
        )
        
        if filepath:
            success, message = import_all_data_json(filepath, self.storage)
            self.import_status.configure(text=message)
    
    def _on_save(self):
        """Save settings."""
        # Update settings
        self.settings.update(
            theme=self.theme_var.get(),
            default_project_color=self.selected_color,
            work_hours_start=self.work_start_entry.get(),
            work_hours_end=self.work_end_entry.get(),
            auto_backup=self.auto_backup_var.get()
        )
        
        # Save to storage
        self.storage.save_settings(self.settings)
        
        # Apply theme
        self.on_theme_change(self.settings.theme)
        
        # Close dialog
        self.destroy()
