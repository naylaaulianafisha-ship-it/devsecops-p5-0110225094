import pytest

from securetask.models import Priority
from securetask.validators import (
    ValidationError, parse_due_date, parse_priority, sanitize_title, validate_tags,
)


def test_sanitize_title_strips_control_chars():
    assert sanitize_title("  Halo\x00  \n dunia ") == "Halo dunia"


@pytest.mark.parametrize("bad", ["", "   ", "a" * 101, 123])
def test_sanitize_title_rejects_invalid(bad):
    with pytest.raises(ValidationError):
        sanitize_title(bad)


def test_parse_priority():
    assert parse_priority("HIGH") is Priority.HIGH
    with pytest.raises(ValidationError):
        parse_priority("urgent")


def test_parse_due_date():
    assert parse_due_date(None) is None
    assert parse_due_date("2026-10-20").year == 2026
    with pytest.raises(ValidationError):
        parse_due_date("20-10-2026")


def test_validate_tags():
    assert validate_tags(["B", "a", "a"]) == ["a", "b"]
    with pytest.raises(ValidationError):
        validate_tags(["bad tag!"])
    with pytest.raises(ValidationError):
        validate_tags(list("abcdef"))
