"""End-to-end tests: migrate into a temporary SQLite DB, then call the FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from scripts.migrate import DATA_DIR, migrate


@pytest.fixture
def client(tmp_path, monkeypatch):
    db = tmp_path / "test.db"
    monkeypatch.setenv("DB_PATH", str(db))
    migrate(DATA_DIR / "students.json", DATA_DIR / "inventory.csv", db)
    from app.main import app

    with TestClient(app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_migrated_students_are_served(client):
    students = client.get("/students").json()
    assert len(students) == 6
    assert students[0] == {"id": 1, "name": "James", "score": 45.0}


def test_student_stats(client):
    stats = client.get("/students/stats").json()
    assert stats["count"] == 6
    assert stats["mean"] == 69.5
    assert stats["highest"]["name"] == "Chinedu"


def test_student_crud(client):
    created = client.post("/students", json={"name": "Bola", "score": 88})
    assert created.status_code == 201
    sid = created.json()["id"]
    assert client.get(f"/students/{sid}").json()["grade"] == "A"
    assert client.put(f"/students/{sid}", json={"name": "Bola", "score": 52}).json()["score"] == 52
    assert client.delete(f"/students/{sid}").status_code == 204
    assert client.get(f"/students/{sid}").status_code == 404


@pytest.mark.parametrize("body", [{"name": "Bola", "score": "90"}, {"name": "Bola", "score": 150}, {"name": "", "score": 50}])
def test_invalid_student_rejected(client, body):
    assert client.post("/students", json=body).status_code == 422


def test_inventory_stats_match_legacy_total(client):
    stats = client.get("/inventory/stats").json()
    assert stats["total_value"] == 10_522_500
    assert [i["item_name"] for i in stats["low_stock"]] == ["Printer"]


def test_inventory_crud_and_conflict(client):
    item = {"item_name": "Webcam", "quantity": 3, "price": 25000.0}
    created = client.post("/inventory", json=item)
    assert created.status_code == 201
    assert client.post("/inventory", json=item).status_code == 409
    iid = created.json()["id"]
    assert client.get(f"/inventory/{iid}").json()["value"] == 75000.0
    assert "Webcam" in [i["item_name"] for i in client.get("/inventory/low-stock").json()]
    assert client.delete(f"/inventory/{iid}").status_code == 204
