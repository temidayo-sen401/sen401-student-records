"""Data migration: legacy JSON/CSV files -> SQLite.

Steps:
  1. Read and validate data/students.json and data/inventory.csv
     (every record passes through the Pydantic models).
  2. Create the SQLite schema if needed.
  3. In one transaction, replace the table contents with the legacy data,
     so running the script again gives the same result (idempotent).
  4. Verify that the row counts and totals in SQLite match the source files.

Usage:
    python3.12 -m scripts.migrate [--students PATH] [--inventory PATH] [--db PATH]
"""

import argparse
import sys
from pathlib import Path

from app.database import connect, db_path, init_db
from app.repository import InventoryRepository, StudentRepository
from app.sources import load_inventory_csv, load_students_json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def migrate(students_path: Path, inventory_path: Path, database: Path) -> None:
    students = load_students_json(students_path)
    items = load_inventory_csv(inventory_path)
    print(f"Read {len(students)} students from {students_path.name}")
    print(f"Read {len(items)} inventory items from {inventory_path.name}")

    conn = connect(database)
    init_db(conn)
    with conn:  # one transaction: all rows are written, or none
        conn.execute("DELETE FROM students")
        conn.execute("DELETE FROM inventory")
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('students', 'inventory')")
        conn.executemany(
            "INSERT INTO students (name, score) VALUES (?, ?)",
            [(s.name, s.score) for s in students],
        )
        conn.executemany(
            "INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)",
            [(i.item_name, i.quantity, i.price) for i in items],
        )

    # Verification: what is in the database must match what was in the files
    db_students = StudentRepository(conn).list()
    db_items = InventoryRepository(conn).list()
    checks = {
        "student count": (len(students), len(db_students)),
        "score total": (sum(s.score for s in students), sum(s.score for s in db_students)),
        "item count": (len(items), len(db_items)),
        "stock value": (
            sum(i.quantity * i.price for i in items),
            sum(i.quantity * i.price for i in db_items),
        ),
    }
    conn.close()

    ok = True
    for name, (source, migrated) in checks.items():
        status = "OK" if source == migrated else "MISMATCH"
        ok &= source == migrated
        print(f"  verify {name:<14} source={source:<12,} sqlite={migrated:<12,} {status}")
    if not ok:
        sys.exit("Migration verification FAILED")
    print(f"Migration complete -> {database}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--students", type=Path, default=DATA_DIR / "students.json")
    parser.add_argument("--inventory", type=Path, default=DATA_DIR / "inventory.csv")
    parser.add_argument("--db", type=Path, default=db_path())
    args = parser.parse_args()
    migrate(args.students, args.inventory, args.db)


if __name__ == "__main__":
    main()
