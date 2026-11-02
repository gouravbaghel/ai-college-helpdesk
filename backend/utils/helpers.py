"""Utility helper functions for the College Helpdesk system."""
import re
from datetime import datetime


def sanitize_filename(filename: str) -> str:
    """Remove special characters from filename."""
    return re.sub(r'[^\w\-.]', '_', filename)


def format_datetime(dt: datetime) -> str:
    """Format datetime object to readable string."""
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "Unknown"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max_length with ellipsis."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
