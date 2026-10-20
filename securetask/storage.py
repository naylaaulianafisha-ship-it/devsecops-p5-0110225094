"""Penyimpanan tugas ke berkas JSON (tanpa deserialisasi tidak aman)."""
import json
import os
import tempfile
from pathlib import Path
from typing import List

from .models import Task


class JsonTaskStorage:
    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)

    def load(self) -> List[Task]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
        return [Task.from_dict(item) for item in raw]

    def save(self, tasks: List[Task]) -> None:
        """Tulis atomik: tulis ke berkas sementara lalu ganti berkas asli."""
        directory = self.path.parent
        directory.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump([t.to_dict() for t in tasks], fh, indent=2)
            os.replace(tmp_name, self.path)
        except Exception:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)
            raise
