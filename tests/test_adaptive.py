"""Tests for adaptive maintenance (issue #4): Pydantic validation."""

import sys

import pytest
from pydantic import ValidationError

from students import Student


def test_running_on_python_312_or_newer():
    assert sys.version_info >= (3, 12)


def test_student_model_accepts_valid_data():
    s = Student(name="Ngozi", score=74)
    assert s.model_dump() == {"name": "Ngozi", "score": 74.0}


@pytest.mark.parametrize(
    "name, score", [("", 50), ("Bola", "90"), ("Bola", 150), ("Bola", -1)]
)
def test_student_model_rejects_invalid_data(name, score):
    with pytest.raises(ValidationError):
        Student(name=name, score=score)
