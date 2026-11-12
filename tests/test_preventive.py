"""Tests for preventive maintenance (issue #6): refactored students.py."""

from students import add_student, average_score, default_students, students


def test_default_students_returns_fresh_copy():
    a = default_students()
    a.append({"name": "X", "score": 1})
    assert len(default_students()) == 5


def test_add_student_to_explicit_list_leaves_shared_list_untouched():
    data = default_students()
    before = len(students)
    record = add_student("Bola", 88, data=data)
    assert record == {"name": "Bola", "score": 88.0}
    assert data[-1] == record
    assert len(students) == before


def test_average_score_empty_returns_float():
    assert average_score([]) == 0.0
    assert isinstance(average_score([]), float)
