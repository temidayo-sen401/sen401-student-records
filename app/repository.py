"""Data access layer: CRUD operations on the SQLite tables.

A single generic :class:`Repository` implements list/get/add/update/delete
for any table (DRY). Each table only declares its name, columns and model.
Table and column names come from these constants, never from user input; all
values are passed as SQL parameters (``?``) to prevent SQL injection.
"""

import sqlite3

from pydantic import BaseModel

from app.models import Item, ItemIn, Student, StudentIn


class Repository[In: BaseModel, Out: BaseModel]:
    """Generic CRUD repository for one table."""

    table: str
    columns: tuple[str, ...]
    model: type[Out]

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def _to_model(self, row: sqlite3.Row) -> Out:
        return self.model.model_validate(dict(row))

    def list(self) -> list[Out]:
        """Return every row, ordered by id."""
        rows = self.conn.execute(f"SELECT * FROM {self.table} ORDER BY id").fetchall()
        return [self._to_model(r) for r in rows]

    def get(self, record_id: int) -> Out | None:
        """Return one row by id, or None if it does not exist."""
        row = self.conn.execute(f"SELECT * FROM {self.table} WHERE id = ?", (record_id,)).fetchone()
        return self._to_model(row) if row else None

    def add(self, data: In) -> Out:
        """Insert a row and return it with its new id."""
        values = data.model_dump()
        placeholders = ", ".join("?" for _ in self.columns)
        cur = self.conn.execute(
            f"INSERT INTO {self.table} ({', '.join(self.columns)}) VALUES ({placeholders})",
            [values[c] for c in self.columns],
        )
        self.conn.commit()
        return self.get(cur.lastrowid)

    def update(self, record_id: int, data: In) -> Out | None:
        """Replace a row's values. Return the updated row, or None if not found."""
        values = data.model_dump()
        assignments = ", ".join(f"{c} = ?" for c in self.columns)
        cur = self.conn.execute(
            f"UPDATE {self.table} SET {assignments} WHERE id = ?",
            [values[c] for c in self.columns] + [record_id],
        )
        self.conn.commit()
        return self.get(record_id) if cur.rowcount else None

    def delete(self, record_id: int) -> bool:
        """Delete a row. Return True if a row was deleted."""
        cur = self.conn.execute(f"DELETE FROM {self.table} WHERE id = ?", (record_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def count(self) -> int:
        """Return the number of rows."""
        return self.conn.execute(f"SELECT COUNT(*) FROM {self.table}").fetchone()[0]


class StudentRepository(Repository[StudentIn, Student]):
    table = "students"
    columns = ("name", "score")
    model = Student


class InventoryRepository(Repository[ItemIn, Item]):
    table = "inventory"
    columns = ("item_name", "quantity", "price")
    model = Item
