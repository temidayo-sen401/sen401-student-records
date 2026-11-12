"""Tests for business rules in app.services (carried over from the legacy suites)."""

import pytest

from app.models import Item, Student
from app.services import grade, inventory_stats, item_value, low_stock, student_stats

STUDENTS = [
    Student(id=1, name="A", score=40),
    Student(id=2, name="B", score=60),
    Student(id=3, name="C", score=80),
    Student(id=4, name="D", score=90),
]
ITEMS = [
    Item(id=1, item_name="A", quantity=2, price=100.0),
    Item(id=2, item_name="B", quantity=50, price=10.0),
    Item(id=3, item_name="C", quantity=8, price=25.0),
]


@pytest.mark.parametrize("score, expected", [(95, "A"), (65, "B"), (55, "C"), (46, "D"), (10, "F")])
def test_grade(score, expected):
    assert grade(score) == expected


def test_student_stats():
    st = student_stats(STUDENTS)
    assert (st.count, st.mean, st.median, st.pass_rate) == (4, 67.5, 70, 75.0)
    assert st.highest.name == "D" and st.lowest.name == "A"


def test_student_stats_empty():
    st = student_stats([])
    assert st.count == 0 and st.highest is None and st.pass_rate == 0.0


def test_item_value_is_quantity_times_price():
    # Regression test for the Lab 3 quantity + price bug
    assert item_value(ITEMS[0]) == 200.0


def test_inventory_stats():
    st = inventory_stats(ITEMS)
    assert st.total_value == 200 + 500 + 200
    assert st.total_units == 60
    assert st.highest_stock.item_name == "B"
    assert st.lowest_stock.item_name == "A"
    assert [i.item_name for i in st.low_stock] == ["A", "C"]


def test_low_stock_threshold():
    assert low_stock(ITEMS, threshold=3) == [ITEMS[0]]
