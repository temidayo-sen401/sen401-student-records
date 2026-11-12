"""Business rules for students and inventory.

Services take model objects and return model objects. They do not know where
the data is stored (file, SQLite, API) or how it is displayed.
"""

from app.models import InventoryStats, Item, Student, StudentStats
from app.utils import describe, highest_by, lowest_by, percentage

PASS_MARK = 50
REORDER_THRESHOLD = 10
# (minimum score, grade), checked from the top down
GRADE_BOUNDARIES: list[tuple[float, str]] = [(70, "A"), (60, "B"), (50, "C"), (45, "D")]


# --- Students -----------------------------------------------------------------

def grade(score: float) -> str:
    """Map a score to a letter grade using GRADE_BOUNDARIES."""
    for minimum, letter in GRADE_BOUNDARIES:
        if score >= minimum:
            return letter
    return "F"


def student_stats(students: list[Student], pass_mark: float = PASS_MARK) -> StudentStats:
    """Return summary statistics for ``students``."""
    stats = describe([s.score for s in students])
    passed = sum(1 for s in students if s.score >= pass_mark)
    return StudentStats(
        count=int(stats["count"]),
        mean=stats["mean"],
        median=stats["median"],
        stdev=stats["stdev"],
        pass_rate=percentage(passed, len(students)),
        highest=highest_by(students, key=lambda s: s.score),
        lowest=lowest_by(students, key=lambda s: s.score),
    )


# --- Inventory ----------------------------------------------------------------

def item_value(item: Item) -> float:
    """Return the stock value of one item (quantity * price)."""
    return item.quantity * item.price


def low_stock(items: list[Item], threshold: int = REORDER_THRESHOLD) -> list[Item]:
    """Return items whose quantity is below ``threshold`` and should be reordered."""
    return [i for i in items if i.quantity < threshold]


def inventory_stats(items: list[Item], threshold: int = REORDER_THRESHOLD) -> InventoryStats:
    """Return summary statistics for ``items``."""
    return InventoryStats(
        item_count=len(items),
        total_units=sum(i.quantity for i in items),
        total_value=sum(item_value(i) for i in items),
        highest_stock=highest_by(items, key=lambda i: i.quantity),
        lowest_stock=lowest_by(items, key=lambda i: i.quantity),
        low_stock=low_stock(items, threshold),
    )
