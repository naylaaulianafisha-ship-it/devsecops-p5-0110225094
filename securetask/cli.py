"""Antarmuka command-line SecureTask."""
import argparse
import sys
from typing import List, Optional

from .service import TaskService
from .storage import JsonTaskStorage
from .validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="securetask",
                                     description="Manajer tugas sederhana")
    parser.add_argument("--file", default="tasks.json", help="berkas penyimpanan")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="tambah tugas")
    add.add_argument("title")
    add.add_argument("--priority", default="medium")
    add.add_argument("--due", help="tenggat (YYYY-MM-DD)")
    add.add_argument("--tag", action="append", default=[])

    ls = sub.add_parser("list", help="tampilkan tugas")
    ls.add_argument("--pending", action="store_true")
    ls.add_argument("--tag")

    done = sub.add_parser("done", help="tandai selesai")
    done.add_argument("id", type=int)

    rm = sub.add_parser("delete", help="hapus tugas")
    rm.add_argument("id", type=int)

    sub.add_parser("stats", help="ringkasan statistik")
    return parser


def run(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(JsonTaskStorage(args.file))
    try:
        if args.command == "add":
            task = service.add_task(args.title, args.priority, args.due, args.tag)
            print(f"Tugas #{task.id} ditambahkan: {task.title}")
        elif args.command == "list":
            for t in service.list_tasks(args.pending, args.tag):
                mark = "x" if t.done else " "
                due = t.due_date.isoformat() if t.due_date else "-"
                print(f"[{mark}] #{t.id} {t.title} ({t.priority.value}, due {due})")
        elif args.command == "done":
            task = service.complete_task(args.id)
            print(f"Tugas #{task.id} selesai")
        elif args.command == "delete":
            service.delete_task(args.id)
            print(f"Tugas #{args.id} dihapus")
        elif args.command == "stats":
            for key, value in service.stats().items():
                print(f"{key}: {value}")
    except (ValidationError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
