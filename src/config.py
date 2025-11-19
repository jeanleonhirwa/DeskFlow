"""
Configuration and constants for Desk Flow application.
"""
import os
from pathlib import Path

# Application Info
APP_NAME = "Desk Flow"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Desk Flow Team"

# Data Directory Paths
HOME_DIR = Path.home()
APP_DATA_DIR = HOME_DIR / ".deskflow"
DATA_DIR = APP_DATA_DIR / "data"
BACKUP_DIR = APP_DATA_DIR / "backups"
LOGS_DIR = APP_DATA_DIR / "logs"

# Data Files
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"
DAILY_PLANS_FILE = DATA_DIR / "daily_plans.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
ANALYTICS_FILE = DATA_DIR / "analytics.json"

# Window Settings
MIN_WINDOW_WIDTH = 1024
MIN_WINDOW_HEIGHT = 768
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 800

# UI Constants
GRID_SIZE = 8
BORDER_RADIUS = 12
SMALL_BORDER_RADIUS = 8
ANIMATION_DURATION = 250  # milliseconds

# Light Mode Colors
LIGHT_THEME = {
    "background": "#FAFAF8",
    "surface": "#FFFFFF",
    "surface_secondary": "#F5F5F0",
    "text_primary": "#2D2D2D",
    "text_secondary": "#6B6B6B",
    "accent": "#E07B53",
    "success": "#4CAF50",
    "warning": "#FFA726",
    "error": "#EF5350",
    "border": "#E0E0E0",
}

# Dark Mode Colors
DARK_THEME = {
    "background": "#1E1E1E",
    "surface": "#2D2D2D",
    "surface_secondary": "#3A3A3A",
    "text_primary": "#E8E8E8",
    "text_secondary": "#A8A8A8",
    "accent": "#F4A261",
    "success": "#66BB6A",
    "warning": "#FFB74D",
    "error": "#EF5350",
    "border": "#4A4A4A",
}

# Font Settings
FONT_FAMILY = "Segoe UI"  # Falls back to system default on other platforms
FONT_SIZE_SMALL = 11
FONT_SIZE_NORMAL = 13
FONT_SIZE_LARGE = 15
FONT_SIZE_HEADING = 18
FONT_SIZE_TITLE = 24

# Default Settings
DEFAULT_SETTINGS = {
    "theme": "system",  # light, dark, or system
    "window_size": {"width": DEFAULT_WINDOW_WIDTH, "height": DEFAULT_WINDOW_HEIGHT},
    "window_position": {"x": 100, "y": 100},
    "default_project_color": "#E07B53",
    "work_hours_start": "09:00",
    "work_hours_end": "17:00",
    "notifications_enabled": True,
    "auto_backup": True,
    "backup_frequency_days": 1,
    "show_completed_tasks": True,
    "task_sort_order": "priority",
    "first_launch": True,
    "last_backup": None,
}

# Project Status Options
PROJECT_STATUS = ["planning", "active", "paused", "completed", "archived"]

# Task Status Options
TASK_STATUS = ["todo", "in_progress", "blocked", "completed"]

# Priority Options
PRIORITY_LEVELS = ["low", "medium", "high"]

# Project Colors (predefined options)
PROJECT_COLORS = [
    "#E07B53",  # Coral Orange
    "#F4A261",  # Warm Orange
    "#4CAF50",  # Green
    "#2196F3",  # Blue
    "#9C27B0",  # Purple
    "#FF5722",  # Deep Orange
    "#00BCD4",  # Cyan
    "#FFEB3B",  # Yellow
    "#795548",  # Brown
    "#607D8B",  # Blue Grey
]

# Backup Settings
MAX_BACKUPS = 7  # Keep 7 days of backups
BACKUP_FILE_PREFIX = "backup_"
