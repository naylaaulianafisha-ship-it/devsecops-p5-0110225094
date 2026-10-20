from datetime import date

from securetask.models import Priority, Task


def test_roundtrip_dict():
    t = Task(1, "Belajar CI", Priority.HIGH, date(2026, 11, 1), tags=["kuliah"])
    assert Task.from_dict(t.to_dict()) == t


def test_overdue_logic():
    t = Task(1, "x", due_date=date(2026, 1, 1))
    assert t.is_overdue(date(2026, 1, 2))
    t.done = True
    assert not t.is_overdue(date(2026, 1, 2))


def test_no_due_date_never_overdue():
    assert not Task(1, "x").is_overdue(date(2030, 1, 1))
