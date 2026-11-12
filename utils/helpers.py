"""Utility functions for working with student records."""

import statistics

from students import StudentRecord


def highest_score(data: list[StudentRecord]) -> StudentRecord | None:
    """Return the student with the highest score, or None if data is empty."""
    if not data:  # Corrective fix: max() raises ValueError on an empty list
        return None
    return max(data, key=lambda s: s["score"])


def lowest_score(data: list[StudentRecord]) -> StudentRecord | None:
    """Return the student with the lowest score, or None if data is empty."""
    if not data:  # Corrective fix: min() raises ValueError on an empty list
        return None
    return min(data, key=lambda s: s["score"])


def pass_rate(data: list[StudentRecord], pass_mark: float = 50) -> float:
    """Return the percentage of students scoring at or above pass_mark."""
    if not data:  # Corrective fix: avoid ZeroDivisionError
        return 0.0
    passed = [s for s in data if s["score"] >= pass_mark]
    return len(passed) / len(data) * 100


def median_score(data: list[StudentRecord]) -> float:
    """Return the median score (Perfective: new statistic)."""
    if not data:
        return 0.0
    return statistics.median(s["score"] for s in data)


def grade(score: float) -> str:
    """Map a score to a letter grade (Perfective: new feature)."""
    if score >= 70:
        return "A"
    if score >= 60:
        return "B"
    if score >= 50:
        return "C"
    if score >= 45:
        return "D"
    return "F"


def score_summary(data: list[StudentRecord]) -> dict[str, float]:
    """Return count, mean, median, standard deviation, min, max and pass rate."""
    scores = [s["score"] for s in data]
    if not scores:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0,
                "min": 0.0, "max": 0.0, "pass_rate": 0.0}
    return {
        "count": len(scores),
        "mean": statistics.fmean(scores),
        "median": statistics.median(scores),
        "stdev": statistics.stdev(scores) if len(scores) > 1 else 0.0,
        "min": min(scores),
        "max": max(scores),
        "pass_rate": pass_rate(data),
    }
