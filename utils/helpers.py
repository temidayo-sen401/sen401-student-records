"""Utility functions for working with student records."""


def highest_score(data):
    """Return the student with the highest score."""
    return max(data, key=lambda s: s["score"])


def lowest_score(data):
    """Return the student with the lowest score."""
    return min(data, key=lambda s: s["score"])


def pass_rate(data, pass_mark=50):
    """Return the percentage of students scoring at or above pass_mark."""
    passed = [s for s in data if s["score"] >= pass_mark]
    return len(passed) / len(data) * 100
