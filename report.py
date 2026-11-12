"""Console report for students and inventory (replaces both legacy app.py scripts).

Presentation only: it loads data, asks the services for statistics and prints.

Usage:  python3.12 report.py
"""

from pathlib import Path

from app.models import Item, Student
from app.services import grade, inventory_stats, item_value, student_stats
from app.sources import load_inventory_csv, load_students_json

DATA_DIR = Path(__file__).parent / "data"
WIDTH = 62


def heading(title: str) -> None:
    """Print a section heading."""
    print("=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)


def print_students(students: list[Student]) -> None:
    """Print a ranked student table and summary statistics."""
    heading("STUDENT RECORDS REPORT")
    print(f"{'#':<4}{'Name':<14}{'Score':>8}{'Grade':>8}")
    for rank, s in enumerate(sorted(students, key=lambda s: s.score, reverse=True), 1):
        print(f"{rank:<4}{s.name:<14}{s.score:>8.1f}{grade(s.score):>8}")
    st = student_stats(students)
    print(f"\nMean {st.mean:.2f} | Median {st.median:.2f} | Std dev {st.stdev:.2f} | Pass rate {st.pass_rate:.1f}%")
    if st.highest and st.lowest:
        print(f"Highest: {st.highest.name} ({st.highest.score:.0f})   Lowest: {st.lowest.name} ({st.lowest.score:.0f})")


def print_inventory(items: list[Item]) -> None:
    """Print the stock table, total value and low-stock alerts."""
    heading("INVENTORY STOCK REPORT")
    print(f"{'Item':<18}{'Qty':>6}{'Unit Price (N)':>17}{'Value (N)':>21}")
    for i in items:
        print(f"{i.item_name:<18}{i.quantity:>6}{i.price:>17,.2f}{item_value(i):>21,.2f}")
    st = inventory_stats(items)
    print(f"{'TOTAL STOCK VALUE':<41}{st.total_value:>21,.2f}")
    for i in st.low_stock:
        print(f"LOW STOCK ALERT: {i.item_name} has only {i.quantity} left - reorder")


def main() -> None:
    """Load the legacy files and print both reports."""
    # Assign ids by position; the data has no ids until it is stored in a database.
    students = [Student(id=n, **s.model_dump()) for n, s in enumerate(load_students_json(DATA_DIR / "students.json"), 1)]
    items = [Item(id=n, **i.model_dump()) for n, i in enumerate(load_inventory_csv(DATA_DIR / "inventory.csv"), 1)]
    print_students(students)
    print()
    print_inventory(items)


if __name__ == "__main__":
    main()
