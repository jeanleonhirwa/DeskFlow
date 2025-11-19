"""
Utility helper functions.
"""
from datetime import datetime
from typing import Optional


def format_date(iso_date: Optional[str], format_str: str = "%b %d, %Y") -> str:
    """Format ISO date string to readable format."""
    if not iso_date:
        return "Not set"
    
    try:
        date = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return date.strftime(format_str)
    except:
        return "Invalid date"


def format_datetime(iso_datetime: Optional[str]) -> str:
    """Format ISO datetime string to readable format."""
    if not iso_datetime:
        return "Not set"
    
    try:
        dt = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return "Invalid datetime"


def time_ago(iso_datetime: Optional[str]) -> str:
    """Convert ISO datetime to 'time ago' format."""
    if not iso_datetime:
        return "Never"
    
    try:
        dt = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days > 1 else ''} ago"
        else:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    except:
        return "Unknown"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def validate_color(color: str) -> bool:
    """Validate hex color format."""
    if not color.startswith("#"):
        return False
    if len(color) != 7:
        return False
    try:
        int(color[1:], 16)
        return True
    except ValueError:
        return False
