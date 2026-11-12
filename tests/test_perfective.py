"""Tests for perfective maintenance (issue #5): new statistics."""

import pytest

from utils.helpers import grade, median_score, score_summary

SAMPLE = [
    {"name": "A", "score": 40},
    {"name": "B", "score": 60},
    {"name": "C", "score": 80},
    {"name": "D", "score": 90},
]


def test_median_score():
    assert median_score(SAMPLE) == 70
    assert median_score([]) == 0.0


@pytest.mark.parametrize(
    "score, expected", [(95, "A"), (65, "B"), (55, "C"), (46, "D"), (10, "F")]
)
def test_grade(score, expected):
    assert grade(score) == expected


def test_score_summary():
    stats = score_summary(SAMPLE)
    assert stats["count"] == 4
    assert stats["mean"] == 67.5
    assert stats["median"] == 70
    assert stats["pass_rate"] == 75.0


def test_score_summary_empty():
    assert score_summary([])["count"] == 0
