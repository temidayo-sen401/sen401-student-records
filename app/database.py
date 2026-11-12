"""SQLite connection handling and schema.

The database file location comes from the ``DB_PATH`` environment variable so
the same code runs locally (``data/school_ops.db``) and in Docker (a volume).
"""

import os
import sqlite3
from collections.abc import Iterator
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "school_ops.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT    NOT NULL,
    score  REAL    NOT NULL CHECK (score BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS inventory (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name  TEXT    NOT NULL UNIQUE,
    quantity   INTEGER NOT NULL CHECK (quantity >= 0),
    price      REAL    NOT NULL CHECK (price >= 0)
);
"""


def db_path() -> Path:
    """Return the database file path (``DB_PATH`` env var, or the default)."""
    return Path(os.getenv("DB_PATH", DEFAULT_DB_PATH))


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    """Open a connection that returns rows as dict-like ``sqlite3.Row`` objects."""
    path = Path(path) if path else db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # check_same_thread=False: FastAPI may run a request's dependency and
    # handler on different worker threads. Each request gets its own connection.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the tables if they do not exist."""
    conn.executescript(SCHEMA)
    conn.commit()


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: one connection per request, always closed afterwards."""
    conn = connect()
    try:
        yield conn
    finally:
        conn.close()
