"""Utility functions for working with student records."""


def highest_score(data):
    """Return the student with the highest score, or None if data is empty."""
    if not data:  # Corrective fix: max() raises ValueError on an empty list
        return None
    return max(data, key=lambda s: s["score"])


def lowest_score(data):
    """Return the student with the lowest score, or None if data is empty."""
    if not data:  # Corrective fix: min() raises ValueError on an empty list
        return None
    return min(data, key=lambda s: s["score"])


def pass_rate(data, pass_mark=50):
    """Return the percentage of students scoring at or above pass_mark."""
    if not data:  # Corrective fix: avoid ZeroDivisionError
        return 0.0
    passed = [s for s in data if s["score"] >= pass_mark]
    return len(passed) / len(data) * 100
