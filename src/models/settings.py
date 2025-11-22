"""
Settings data model for Desk Flow.
"""
from typing import Dict, Any
from datetime import datetime


class Settings:
    """Application settings."""
    
    def __init__(self, settings_dict: Dict[str, Any]):
        self.theme = settings_dict.get("theme", "system")
        self.window_size = settings_dict.get("window_size", {"width": 1280, "height": 800})
        self.window_position = settings_dict.get("window_position", {"x": 100, "y": 100})
        self.default_project_color = settings_dict.get("default_project_color", "#E07B53")
        self.work_hours_start = settings_dict.get("work_hours_start", "09:00")
        self.work_hours_end = settings_dict.get("work_hours_end", "17:00")
        self.notifications_enabled = settings_dict.get("notifications_enabled", True)
        self.auto_backup = settings_dict.get("auto_backup", True)
        self.backup_frequency_days = settings_dict.get("backup_frequency_days", 1)
        self.show_completed_tasks = settings_dict.get("show_completed_tasks", True)
        self.task_sort_order = settings_dict.get("task_sort_order", "priority")
        self.first_launch = settings_dict.get("first_launch", True)
        self.last_backup = settings_dict.get("last_backup")
        
        # Notification settings
        self.notification_settings = settings_dict.get("notification_settings", {
            "enabled": True,
            "task_due_soon": True,
            "task_overdue": True,
            "daily_summary": True,
            "daily_summary_time": "09:00",
            "notification_duration": 5000
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary for JSON serialization."""
        return {
            "theme": self.theme,
            "window_size": self.window_size,
            "window_position": self.window_position,
            "default_project_color": self.default_project_color,
            "work_hours_start": self.work_hours_start,
            "work_hours_end": self.work_hours_end,
            "notifications_enabled": self.notifications_enabled,
            "auto_backup": self.auto_backup,
            "backup_frequency_days": self.backup_frequency_days,
            "show_completed_tasks": self.show_completed_tasks,
            "task_sort_order": self.task_sort_order,
            "first_launch": self.first_launch,
            "last_backup": self.last_backup,
            "notification_settings": self.notification_settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Settings":
        """Create settings instance from dictionary."""
        return cls(data)
    
    def update(self, **kwargs):
        """Update settings."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
