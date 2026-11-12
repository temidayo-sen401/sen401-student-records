"""Generic helper functions that work for any domain (students, inventory, ...).

They replace the near-identical helpers each legacy app had (DRY):
``highest_score``/``highest_stock_item`` both became :func:`highest_by`, and
``lowest_score``/``lowest_stock_item`` both became :func:`lowest_by`.
This module depends on nothing else in the project.
"""

import statistics
from collections.abc import Callable, Sequence


def highest_by[T](items: Sequence[T], key: Callable[[T], float]) -> T | None:
    """Return the item with the largest ``key`` value, or None if ``items`` is empty."""
    return max(items, key=key) if items else None


def lowest_by[T](items: Sequence[T], key: Callable[[T], float]) -> T | None:
    """Return the item with the smallest ``key`` value, or None if ``items`` is empty."""
    return min(items, key=key) if items else None


def percentage(part: int, whole: int) -> float:
    """Return ``part`` as a percentage of ``whole`` (0.0 when ``whole`` is 0)."""
    return part / whole * 100 if whole else 0.0


def describe(values: Sequence[float]) -> dict[str, float]:
    """Return count, mean, median and sample standard deviation of ``values``."""
    if not values:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0}
    return {
        "count": len(values),
        "mean": statistics.fmean(values),
        "median": float(statistics.median(values)),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
    }
