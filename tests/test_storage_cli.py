from securetask.cli import run
from securetask.models import Task
from securetask.storage import JsonTaskStorage


def test_storage_load_missing_returns_empty(tmp_path):
    assert JsonTaskStorage(str(tmp_path / "none.json")).load() == []


def test_storage_save_load(tmp_path):
    s = JsonTaskStorage(str(tmp_path / "d" / "t.json"))
    s.save([Task(1, "x")])
    assert s.load()[0].title == "x"


def test_cli_flow(tmp_path, capsys):
    f = str(tmp_path / "t.json")
    assert run(["--file", f, "add", "Tugas P5", "--priority", "high", "--tag", "kuliah"]) == 0
    assert run(["--file", f, "list"]) == 0
    assert "Tugas P5" in capsys.readouterr().out
    assert run(["--file", f, "done", "1"]) == 0
    assert run(["--file", f, "stats"]) == 0
    assert run(["--file", f, "delete", "1"]) == 0


def test_cli_error_returns_1(tmp_path):
    f = str(tmp_path / "t.json")
    assert run(["--file", f, "add", "x", "--priority", "bogus"]) == 1
    assert run(["--file", f, "done", "42"]) == 1
