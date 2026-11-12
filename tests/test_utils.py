"""Tests for the generic helpers in app.utils."""

from app.utils import describe, highest_by, lowest_by, percentage


def test_highest_and_lowest_by_work_for_any_key():
    data = [("a", 3), ("b", 9), ("c", 1)]
    assert highest_by(data, key=lambda x: x[1]) == ("b", 9)
    assert lowest_by(data, key=lambda x: x[1]) == ("c", 1)


def test_highest_and_lowest_by_empty():
    assert highest_by([], key=len) is None
    assert lowest_by([], key=len) is None


def test_percentage():
    assert percentage(1, 4) == 25.0
    assert percentage(1, 0) == 0.0


def test_describe():
    stats = describe([40, 60, 80, 90])
    assert stats["count"] == 4
    assert stats["mean"] == 67.5
    assert stats["median"] == 70
    assert describe([])["count"] == 0
    assert describe([5])["stdev"] == 0.0
