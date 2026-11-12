"""Tests for model validation and the legacy JSON/CSV readers."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from app.models import ItemIn, StudentIn
from app.sources import load_inventory_csv, load_students_json

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.mark.parametrize("name, score", [("", 50), ("Bola", "90"), ("Bola", 150), ("Bola", -1)])
def test_student_rejects_invalid(name, score):
    with pytest.raises(ValidationError):
        StudentIn(name=name, score=score)


@pytest.mark.parametrize("qty, price", [(-1, 10.0), ("5", 10.0), (5, -2.0)])
def test_item_rejects_invalid(qty, price):
    with pytest.raises(ValidationError):
        ItemIn(item_name="X", quantity=qty, price=price)


def test_load_legacy_files():
    students = load_students_json(DATA / "students.json")
    items = load_inventory_csv(DATA / "inventory.csv")
    assert len(students) == 6 and students[0].name == "James"
    assert len(items) == 6 and items[-1].item_name == "Printer"
