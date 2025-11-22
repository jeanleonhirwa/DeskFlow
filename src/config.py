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

# Light Mode Colors (Enhanced v2)
LIGHT_THEME = {
    "background": "#F8F9FA",  # Softer white background
    "surface": "#FFFFFF",
    "surface_secondary": "#F1F3F4",  # Slightly darker for contrast
    "surface_hover": "#E8EAED",  # Hover state for interactive elements
    "text_primary": "#202124",  # Darker for better contrast (WCAG AA)
    "text_secondary": "#5F6368",  # Medium gray
    "text_tertiary": "#80868B",  # Light gray for less important text
    "accent": "#D93025",  # More vibrant red-orange
    "accent_hover": "#C5221F",  # Darker on hover
    "success": "#1E8E3E",  # Richer green
    "warning": "#F9AB00",  # Warmer yellow
    "error": "#D93025",  # Red
    "border": "#DADCE0",  # Light border
    "border_focus": "#1A73E8",  # Blue for focused elements
    "shadow": "rgba(0, 0, 0, 0.1)"  # Subtle shadow for elevation
}

# Dark Mode Colors (Enhanced v2)
DARK_THEME = {
    "background": "#121212",  # True dark background
    "surface": "#1E1E1E",  # Slightly lighter surface
    "surface_secondary": "#2A2A2A",  # Even lighter for hierarchy
    "surface_hover": "#353535",  # Hover state
    "text_primary": "#E8EAED",  # High contrast text
    "text_secondary": "#9AA0A6",  # Medium gray
    "text_tertiary": "#70757A",  # Dimmer text
    "accent": "#8AB4F8",  # Softer blue (easier on eyes in dark)
    "accent_hover": "#AECBFA",  # Lighter blue on hover
    "success": "#81C995",  # Softer green
    "warning": "#FDD663",  # Softer yellow
    "error": "#F28B82",  # Softer red
    "border": "#3C4043",  # Dark border
    "border_focus": "#8AB4F8",  # Blue focus indicator
    "shadow": "rgba(0, 0, 0, 0.3)"  # Deeper shadow for dark mode
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
