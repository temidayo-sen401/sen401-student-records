"""Baseline tests for utils.helpers and students (v1.0)."""

from students import average_score
from utils.helpers import highest_score, lowest_score, pass_rate

SAMPLE = [
    {"name": "A", "score": 40},
    {"name": "B", "score": 60},
    {"name": "C", "score": 80},
]


def test_highest_score():
    assert highest_score(SAMPLE)["name"] == "C"


def test_lowest_score():
    assert lowest_score(SAMPLE)["name"] == "A"


def test_pass_rate():
    assert round(pass_rate(SAMPLE), 2) == 66.67


def test_average_score():
    assert average_score(SAMPLE) == 60


def test_average_score_empty():
    assert average_score([]) == 0
