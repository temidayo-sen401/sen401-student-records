"""REST endpoints for inventory: /inventory."""

import sqlite3
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.models import InventoryStats, Item, ItemIn
from app.repository import InventoryRepository
from app.services import REORDER_THRESHOLD, inventory_stats, item_value, low_stock

router = APIRouter(prefix="/inventory", tags=["inventory"])


def get_repo(conn: Annotated[sqlite3.Connection, Depends(get_db)]) -> InventoryRepository:
    return InventoryRepository(conn)


Repo = Annotated[InventoryRepository, Depends(get_repo)]


def _not_found(item_id: int) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")


@router.get("", response_model=list[Item])
def list_items(repo: Repo):
    """List all inventory items."""
    return repo.list()


@router.get("/stats", response_model=InventoryStats)
def get_inventory_stats(repo: Repo, threshold: Annotated[int, Query(ge=0)] = REORDER_THRESHOLD):
    """Total stock value, total units, highest/lowest stock and low-stock items."""
    return inventory_stats(repo.list(), threshold)


@router.get("/low-stock", response_model=list[Item])
def get_low_stock(repo: Repo, threshold: Annotated[int, Query(ge=0)] = REORDER_THRESHOLD):
    """Items below the reorder threshold."""
    return low_stock(repo.list(), threshold)


@router.get("/{item_id}")
def get_item(item_id: int, repo: Repo) -> dict:
    """Get one item, including its stock value."""
    item = repo.get(item_id)
    if item is None:
        raise _not_found(item_id)
    return {**item.model_dump(), "value": item_value(item)}


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemIn, repo: Repo):
    """Add an item. Item names must be unique (409 if the name already exists)."""
    try:
        return repo.add(data)
    except sqlite3.IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Item '{data.item_name}' already exists")


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, data: ItemIn, repo: Repo):
    """Replace an item's name, quantity and price."""
    try:
        item = repo.update(item_id, data)
    except sqlite3.IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Item '{data.item_name}' already exists")
    if item is None:
        raise _not_found(item_id)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, repo: Repo) -> None:
    """Delete an item."""
    if not repo.delete(item_id):
        raise _not_found(item_id)
