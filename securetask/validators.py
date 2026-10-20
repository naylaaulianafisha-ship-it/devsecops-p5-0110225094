"""Validasi dan sanitasi input pengguna."""
import re
from datetime import date
from typing import Optional

from .models import Priority

MAX_TITLE_LENGTH = 100
MAX_TAGS = 5
_TAG_PATTERN = re.compile(r"^[a-z0-9_-]{1,20}$")
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


class ValidationError(ValueError):
    """Dilempar ketika input tidak valid."""


def sanitize_title(title: str) -> str:
    """Hapus karakter kontrol, rapikan spasi, dan batasi panjang judul."""
    if not isinstance(title, str):
        raise ValidationError("Judul harus berupa teks")
    cleaned = _CONTROL_CHARS.sub(" ", title).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    if not cleaned:
        raise ValidationError("Judul tidak boleh kosong")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise ValidationError(f"Judul maksimal {MAX_TITLE_LENGTH} karakter")
    return cleaned


def parse_priority(value: str) -> Priority:
    try:
        return Priority(value.lower())
    except (ValueError, AttributeError) as exc:
        raise ValidationError(f"Prioritas tidak valid: {value!r}") from exc


def parse_due_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError("Format tanggal harus YYYY-MM-DD") from exc


def validate_tags(tags: Optional[list]) -> list:
    tags = [t.strip().lower() for t in (tags or []) if t and t.strip()]
    tags = sorted(set(tags))
    if len(tags) > MAX_TAGS:
        raise ValidationError(f"Maksimal {MAX_TAGS} tag")
    for tag in tags:
        if not _TAG_PATTERN.match(tag):
            raise ValidationError(f"Tag tidak valid: {tag!r}")
    return tags
