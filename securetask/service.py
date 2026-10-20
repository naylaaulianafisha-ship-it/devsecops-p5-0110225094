"""Logika bisnis SecureTask."""
from datetime import date
from typing import Dict, List, Optional

from .models import Priority, Task
from .storage import JsonTaskStorage
from .validators import (
    parse_due_date,
    parse_priority,
    sanitize_title,
    validate_tags,
)

_PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}


class TaskService:
    def __init__(self, storage: JsonTaskStorage):
        self.storage = storage

    def add_task(self, title: str, priority: str = "medium",
                 due: Optional[str] = None, tags: Optional[list] = None) -> Task:
        tasks = self.storage.load()
        new_id = max((t.id for t in tasks), default=0) + 1
        task = Task(
            id=new_id,
            title=sanitize_title(title),
            priority=parse_priority(priority),
            due_date=parse_due_date(due),
            tags=validate_tags(tags),
        )
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def complete_task(self, task_id: int) -> Task:
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.storage.save(tasks)
                return task
        raise KeyError(f"Tugas dengan id {task_id} tidak ditemukan")

    def delete_task(self, task_id: int) -> None:
        tasks = self.storage.load()
        remaining = [t for t in tasks if t.id != task_id]
        if len(remaining) == len(tasks):
            raise KeyError(f"Tugas dengan id {task_id} tidak ditemukan")
        self.storage.save(remaining)

    def list_tasks(self, only_pending: bool = False,
                   tag: Optional[str] = None) -> List[Task]:
        tasks = self.storage.load()
        if only_pending:
            tasks = [t for t in tasks if not t.done]
        if tag:
            tasks = [t for t in tasks if tag.lower() in t.tags]
        return sorted(tasks, key=lambda t: (_PRIORITY_ORDER[t.priority], t.id))

    def stats(self, today: Optional[date] = None) -> Dict[str, int]:
        tasks = self.storage.load()
        return {
            "total": len(tasks),
            "done": sum(1 for t in tasks if t.done),
            "pending": sum(1 for t in tasks if not t.done),
            "overdue": sum(1 for t in tasks if t.is_overdue(today)),
        }
