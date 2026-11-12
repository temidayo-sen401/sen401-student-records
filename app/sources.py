"""Readers for the legacy flat-file data sources (JSON and CSV).

Every record is validated with the Pydantic ``*In`` models, so bad data is
rejected when it is loaded rather than failing later in a calculation.
"""

import csv
import json
from pathlib import Path

from app.models import ItemIn, StudentIn


def load_students_json(path: str | Path) -> list[StudentIn]:
    """Load and validate students from a JSON array of {name, score} objects."""
    with Path(path).open(encoding="utf-8") as f:
        return [StudentIn.model_validate(row) for row in json.load(f)]


def load_inventory_csv(path: str | Path) -> list[ItemIn]:
    """Load and validate items from a CSV file with item_name, quantity, price columns."""
    with Path(path).open(newline="", encoding="utf-8") as f:
        return [
            ItemIn(
                item_name=row["item_name"],
                quantity=int(row["quantity"]),
                price=float(row["price"]),
            )
            for row in csv.DictReader(f)
        ]
