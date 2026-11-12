"""Data models (Pydantic schemas) shared by every layer of the application.

``*In`` models describe what a client sends (no id); the plain models add the
database id and are returned to clients. This module depends on nothing else
in the project.
"""

from pydantic import BaseModel, Field

MIN_SCORE = 0
MAX_SCORE = 100


# --- Students -----------------------------------------------------------------

class StudentIn(BaseModel):
    """A student as submitted by a client."""

    name: str = Field(min_length=1, max_length=100, examples=["Ngozi"])
    score: float = Field(ge=MIN_SCORE, le=MAX_SCORE, strict=True, examples=[74])


class Student(StudentIn):
    """A stored student."""

    id: int


class StudentStats(BaseModel):
    """Summary statistics for a set of students."""

    count: int
    mean: float
    median: float
    stdev: float
    pass_rate: float
    highest: Student | None
    lowest: Student | None


# --- Inventory ----------------------------------------------------------------

class ItemIn(BaseModel):
    """An inventory item as submitted by a client."""

    item_name: str = Field(min_length=1, max_length=100, examples=["Laptop"])
    quantity: int = Field(ge=0, strict=True, examples=[12])
    price: float = Field(ge=0, strict=True, examples=[450000.0])


class Item(ItemIn):
    """A stored inventory item."""

    id: int


class InventoryStats(BaseModel):
    """Summary statistics for the inventory."""

    item_count: int
    total_units: int
    total_value: float
    highest_stock: Item | None
    lowest_stock: Item | None
    low_stock: list[Item]
