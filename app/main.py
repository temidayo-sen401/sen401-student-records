"""FastAPI application entry point.

Run locally:  uvicorn app.main:app --reload
Interactive API docs: http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import inventory, students
from app.database import connect, db_path, init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Make sure the tables exist before the first request."""
    conn = connect()
    init_db(conn)
    conn.close()
    yield


app = FastAPI(
    title="School Ops API",
    version="2.0.0",
    description="Re-engineered Student Records and Inventory system (SEN 401, Lab 4).",
    lifespan=lifespan,
)
app.include_router(students.router)
app.include_router(inventory.router)


@app.get("/health", tags=["system"])
def health() -> dict:
    """Liveness check used by Docker Compose."""
    return {"status": "ok", "database": str(db_path())}
