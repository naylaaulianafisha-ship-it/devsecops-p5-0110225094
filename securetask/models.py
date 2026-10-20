"""Model data untuk SecureTask."""
from dataclasses import dataclass, asdict, field
from datetime import date
from enum import Enum
from typing import Optional


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    due_date: Optional[date] = None
    done: bool = False
    tags: list = field(default_factory=list)

    def is_overdue(self, today: Optional[date] = None) -> bool:
        """Tugas dianggap terlambat jika belum selesai dan lewat tenggat."""
        today = today or date.today()
        return (not self.done) and self.due_date is not None and self.due_date < today

    def to_dict(self) -> dict:
        data = asdict(self)
        data["priority"] = self.priority.value
        data["due_date"] = self.due_date.isoformat() if self.due_date else None
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        due = data.get("due_date")
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            priority=Priority(data.get("priority", "medium")),
            due_date=date.fromisoformat(due) if due else None,
            done=bool(data.get("done", False)),
            tags=list(data.get("tags", [])),
        )
