from datetime import date

import pytest

from securetask.service import TaskService
from securetask.storage import JsonTaskStorage


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonTaskStorage(str(tmp_path / "tasks.json")))


def test_add_and_list_sorted_by_priority(service):
    service.add_task("rendah", "low")
    service.add_task("tinggi", "high")
    assert [t.title for t in service.list_tasks()] == ["tinggi", "rendah"]


def test_complete_and_filter_pending(service):
    t = service.add_task("a")
    service.add_task("b")
    service.complete_task(t.id)
    assert [x.title for x in service.list_tasks(only_pending=True)] == ["b"]


def test_filter_by_tag(service):
    service.add_task("a", tags=["kuliah"])
    service.add_task("b")
    assert len(service.list_tasks(tag="kuliah")) == 1


def test_delete_and_missing(service):
    t = service.add_task("a")
    service.delete_task(t.id)
    assert service.list_tasks() == []
    with pytest.raises(KeyError):
        service.delete_task(99)
    with pytest.raises(KeyError):
        service.complete_task(99)


def test_stats(service):
    service.add_task("a", due="2020-01-01")
    t = service.add_task("b")
    service.complete_task(t.id)
    s = service.stats(today=date(2026, 1, 1))
    assert s == {"total": 2, "done": 1, "pending": 1, "overdue": 1}
