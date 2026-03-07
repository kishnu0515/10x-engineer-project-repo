import pytest
import uuid
from datetime import datetime, timedelta

from app.utils import (
    generate_id,
    validate_uuid,
    sanitize_string,
    normalize_search_query,
    validate_string_length,
    get_current_timestamp,
    calculate_time_difference,
    truncate_string,
    format_error_response,
)


# =========================
# generate_id
# =========================

def test_generate_id_format_and_uniqueness():
    id1 = generate_id()
    id2 = generate_id()
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    assert len(id1) == 36
    assert id1 != id2
    # validate it is UUID
    assert validate_uuid(id1) is True


# =========================
# validate_uuid
# =========================

def test_validate_uuid_valid_and_invalid():
    valid = str(uuid.uuid4())
    assert validate_uuid(valid) is True
    assert validate_uuid("invalid-uuid") is False


def test_validate_uuid_raises_on_empty_or_none():
    with pytest.raises(ValueError):
        validate_uuid("")
    with pytest.raises(ValueError):
        validate_uuid(None)  # type: ignore[arg-type]


# =========================
# sanitize_string
# =========================

def test_sanitize_string_trims_whitespace():
    assert sanitize_string("  Hello World  ") == "Hello World"
    assert sanitize_string("\n\tTrim Me\t\n") == "Trim Me"


def test_sanitize_string_raises_on_none():
    with pytest.raises(ValueError):
        sanitize_string(None)  # type: ignore[arg-type]


# =========================
# normalize_search_query
# =========================

def test_normalize_search_query_lowercases_and_trims():
    assert normalize_search_query("  PyThOn  ") == "python"


def test_normalize_search_query_raises_on_none():
    with pytest.raises(ValueError):
        normalize_search_query(None)  # type: ignore[arg-type]


# =========================
# validate_string_length
# =========================

def test_validate_string_length_happy_paths():
    assert validate_string_length("abc", min_length=1, max_length=5) is True
    assert validate_string_length("a", min_length=1) is True


def test_validate_string_length_edge_cases():
    assert validate_string_length("a", min_length=2) is False
    assert validate_string_length("abcdef", max_length=5) is False


def test_validate_string_length_raises_on_none():
    with pytest.raises(ValueError):
        validate_string_length(None)  # type: ignore[arg-type]


# =========================
# get_current_timestamp
# =========================

def test_get_current_timestamp_is_recent_datetime():
    ts = get_current_timestamp()
    assert isinstance(ts, datetime)
    # naive UTC datetime close to now
    now = datetime.utcnow()
    assert abs((now - ts).total_seconds()) < 2


# =========================
# calculate_time_difference
# =========================

def test_calculate_time_difference_seconds():
    start = datetime(2024, 1, 1, 12, 0, 0)
    end = datetime(2024, 1, 1, 12, 5, 30)
    assert calculate_time_difference(start, end) == 330.0


def test_calculate_time_difference_negative():
    a = datetime(2024, 1, 1, 12, 0, 1)
    b = datetime(2024, 1, 1, 12, 0, 0)
    assert calculate_time_difference(a, b) == -1.0


def test_calculate_time_difference_type_errors():
    with pytest.raises(TypeError):
        calculate_time_difference("not-dt", datetime.utcnow())  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        calculate_time_difference(datetime.utcnow(), "not-dt")  # type: ignore[arg-type]


# =========================
# truncate_string
# =========================

def test_truncate_string_no_truncation_when_within_limit():
    assert truncate_string("Hello", max_length=10) == "Hello"


def test_truncate_string_with_default_suffix():
    result = truncate_string("Hello World", max_length=8)
    assert result == "Hello..."
    assert len(result) == 8


def test_truncate_string_with_custom_suffix():
    result = truncate_string("abcdefghij", max_length=6, suffix=">")
    assert result == "abcde>"
    assert len(result) == 6


def test_truncate_string_errors():
    with pytest.raises(TypeError):
        truncate_string(123, max_length=5)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        truncate_string("Test", max_length=2, suffix="...")


# =========================
# format_error_response
# =========================

def test_format_error_response_structure_and_defaults():
    err = format_error_response("INVALID_ID", "ID is invalid")
    assert err["error_code"] == "INVALID_ID"
    assert err["error_message"] == "ID is invalid"
    assert isinstance(err["details"], dict) and err["details"] == {}
    # Validate timestamp is ISO format
    datetime.fromisoformat(err["timestamp"])  # should not raise


def test_format_error_response_with_details():
    details = {"field": "id", "reason": "bad format"}
    err = format_error_response("VALIDATION_ERROR", "Bad input", details)
    assert err["details"] == details