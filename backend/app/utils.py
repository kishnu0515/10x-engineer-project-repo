"""Utility functions for PromptLab"""

import uuid
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_id() -> str:
    """Generate a unique identifier using UUID4.
    
    Returns:
        str: A string representation of a UUID4.
        
    Example:
        >>> id = generate_id()
        >>> len(id)
        36
        >>> isinstance(id, str)
        True
    """
    return str(uuid.uuid4())


def validate_uuid(uuid_string: str) -> bool:
    """Validate if a string is a valid UUID.
    
    Args:
        uuid_string: The string to validate as a UUID.
        
    Returns:
        bool: True if valid UUID format, False otherwise.
        
    Raises:
        ValueError: If uuid_string is None or empty.
        
    Example:
        >>> validate_uuid("550e8400-e29b-41d4-a716-446655440000")
        True
        >>> validate_uuid("invalid-uuid")
        False
    """
    if not uuid_string:
        raise ValueError("UUID string cannot be empty or None")
    
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, AttributeError):
        return False


def sanitize_string(input_str: str) -> str:
    """Sanitize a string by stripping whitespace.
    
    Args:
        input_str: The string to sanitize.
        
    Returns:
        str: The sanitized string with leading/trailing whitespace removed.
        
    Raises:
        ValueError: If input_str is None.
        
    Example:
        >>> sanitize_string("  Hello World  ")
        'Hello World'
        >>> sanitize_string("\t\nTest\n\t")
        'Test'
    """
    if input_str is None:
        raise ValueError("Input string cannot be None")
    
    return input_str.strip()


def normalize_search_query(query: str) -> str:
    """Normalize a search query for consistent filtering.
    
    Sanitizes and converts to lowercase for case-insensitive search.
    
    Args:
        query: The raw search query string.
        
    Returns:
        str: The normalized search query.
        
    Raises:
        ValueError: If query is None.
        
    Example:
        >>> normalize_search_query("  PYTHON TUTORIAL  ")
        'python tutorial'
        >>> normalize_search_query("FastAPI")
        'fastapi'
    """
    if query is None:
        raise ValueError("Search query cannot be None")
    
    return sanitize_string(query).lower()


def validate_string_length(value: str, min_length: int = 1, max_length: Optional[int] = None) -> bool:
    """Validate that a string meets length requirements.
    
    Args:
        value: The string to validate.
        min_length: Minimum required length (inclusive), default 1.
        max_length: Maximum allowed length (inclusive), None for unlimited.
        
    Returns:
        bool: True if string meets requirements, False otherwise.
        
    Raises:
        ValueError: If value is None.
        
    Example:
        >>> validate_string_length("hello", min_length=1, max_length=10)
        True
        >>> validate_string_length("x", min_length=2)
        False
        >>> validate_string_length("toolong", max_length=5)
        False
    """
    if value is None:
        raise ValueError("String value cannot be None")
    
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    return True


def get_current_timestamp() -> datetime:
    """Get the current UTC timestamp.
    
    Returns:
        datetime: The current datetime in UTC.
        
    Example:
        >>> now = get_current_timestampstamp()
        >>> isinstance(now, datetime)
        True
        >>> now.tzinfo is None or str(now.tzinfo) == 'UTC'
        True
    """
    return datetime.utcnow()


def calculate_time_difference(start: datetime, end: datetime) -> float:
    """Calculate the difference between two datetimes in seconds.
    
    Args:
        start: The start datetime.
        end: The end datetime.
        
    Returns:
        float: The difference in seconds (can be negative if end < start).
        
    Raises:
        TypeError: If start or end are not datetime objects.
        
    Example:
        >>> start = datetime(2024, 1, 1, 12, 0, 0)
        >>> end = datetime(2024, 1, 1, 12, 5, 30)
        >>> calculate_time_difference(start, end)
        330.0
    """
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("Both arguments must be datetime objects")
    
    delta = end - start
    return delta.total_seconds()


def truncate_string(value: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to a maximum length with optional suffix.
    
    Args:
        value: The string to truncate.
        max_length: Maximum length of the returned string (including suffix).
        suffix: String to append if truncated, default "...".
        
    Returns:
        str: The truncated string, or original if already short enough.
        
    Raises:
        ValueError: If max_length is less than suffix length.
        TypeError: If value is not a string.
        
    Example:
        >>> truncate_string("Hello World", max_length=8)
        'Hello...'
        >>> truncate_string("Hi", max_length=10)
        'Hi'
        >>> truncate_string("Test", max_length=6, suffix=">")
        'Test>'
    """
    if not isinstance(value, str):
        raise TypeError("Value must be a string")
    
    if max_length < len(suffix):
        raise ValueError("max_length must be greater than suffix length")
    
    if len(value) <= max_length:
        return value
    
    return value[:max_length - len(suffix)] + suffix


def format_error_response(error_code: str, error_message: str, details: Optional[dict] = None) -> dict:
    """Format a consistent error response structure.
    
    Args:
        error_code: The error code (e.g., "VALIDATION_ERROR", "NOT_FOUND").
        error_message: Human-readable error message.
        details: Optional dictionary with additional error details.
        
    Returns:
        dict: Formatted error response.
        
    Example:
        >>> error = format_error_response("INVALID_ID", "Prompt ID is invalid")
        >>> error['error_code']
        'INVALID_ID'
        >>> error['timestamp']  # Contains ISO format timestamp
        '2024-...'
    """
    return {
        "error_code": error_code,
        "error_message": error_message,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }
